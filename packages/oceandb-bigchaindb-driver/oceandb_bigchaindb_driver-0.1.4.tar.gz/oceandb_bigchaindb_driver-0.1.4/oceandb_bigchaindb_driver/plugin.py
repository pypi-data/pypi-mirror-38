"""Implementation of OceanDB plugin based in BigchainDB"""
import json
import logging

import requests
from bigchaindb_driver.exceptions import BadRequest
from oceandb_driver_interface.plugin import AbstractPlugin
from oceandb_driver_interface.search_model import FullTextModel, QueryModel

from oceandb_bigchaindb_driver.instance import get_database_instance, generate_key_pair, get_value


class Plugin(AbstractPlugin):
    """BigchainDB ledger plugin for `Ocean DB's Python reference
    implementation <https://github.com/oceanprotocol/oceandb-bigchaindb-driver>`_.
    Plugs in a BigchainDB instance as the persistence layer for Ocean Db
    related actions.
    """
    BURN_ADDRESS = 'BurnBurnBurnBurnBurnBurnBurnBurnBurnBurnBurn'

    def __init__(self, config=None, namespace=None):
        """Initialize a :class:`~.Plugin` instance and connect to BigchainDB.
        Args:
            *nodes (str): One or more URLs of BigchainDB nodes to
                connect to as the persistence layer
        """
        self.driver = get_database_instance(config)
        self.user = generate_key_pair(get_value('secret', 'SECRET', None, config))
        self.namespace = get_value('db.namespace', 'DB_NAMESPACE', 'namespace' if not namespace else namespace, config)
        self.logger = logging.getLogger('Plugin')
        logging.basicConfig(level=logging.INFO)

    @property
    def type(self):
        """str: the type of this plugin (``'BigchainDB'``)"""
        return 'BigchainDB'

    def write(self, obj, resource_id=None):
        """Write and obj in bdb.

        :param obj: value to be written in bdb.
        :param resource_id: id to make possible read and search for an resource.
        :return: id of the transaction
        """
        if resource_id is not None:
            if self.read(resource_id):
                raise ValueError("There are one object already with this id.")
            obj['_id'] = resource_id
        prepared_creation_tx = self.driver.instance.transactions.prepare(
            operation='CREATE',
            signers=self.user.public_key,
            asset={
                'namespace': self.namespace,
                'data': obj
            },
            metadata={
                'namespace': self.namespace,
                'data': obj
            }
        )

        signed_tx = self.driver.instance.transactions.fulfill(
            prepared_creation_tx,
            private_keys=self.user.private_key
        )
        self.logger.debug('bdb::write::{}'.format(signed_tx['id']))
        self.driver.instance.transactions.send(signed_tx)
        return signed_tx

    def read(self, resource_id):
        tx_id = self._find_tx_id(resource_id)
        if not tx_id:
            return False
        return self._get(tx_id)['data']['data']

    def _get(self, tx_id):
        """Read and obj in bdb using the tx_id.

        :param resource_id: id of the transaction to be read.
        :return: value with the data, transaction id and transaction.
        """
        # tx_id=self._find_tx_id(resource_id)
        value = [
            {
                'data': transaction['metadata'],
                'id': transaction['id']
            }
            for transaction in self.driver.instance.transactions.get(asset_id=self.get_asset_id(tx_id))
        ][-1]
        if value['data']['data']:
            self.logger.debug('bdb::read::{}'.format(value['data']))
            return value
        else:
            return False

    def update(self, record, asset_id):
        tx_id = self._find_tx_id(asset_id)
        return self._update(record, tx_id, asset_id)

    def _update(self, metadata, tx_id, resource_id):
        """Update and obj in bdb using the tx_id.

        :param metadata: new metadata for the transaction.
        :param tx_id: id of the transaction to be updated.
        :return: id of the transaction.
        """
        try:
            if not tx_id:
                sent_tx = self.write(metadata, resource_id)
                self.logger.debug('bdb::put::{}'.format(sent_tx['id']))
                return sent_tx
            else:
                txs = self.driver.instance.transactions.get(asset_id=self.get_asset_id(tx_id))
                unspent = txs[-1]
                sent_tx = self._put(metadata, unspent, resource_id)
                self.logger.debug('bdb::put::{}'.format(sent_tx))
                return sent_tx

        except BadRequest as e:
            logging.error(e)

    def list(self, search_from=None, search_to=None, limit=None):
        """List all the objects saved in the namespace.

         :param search_from: TBI
         :param search_to: TBI
         :param offset: TBI
         :param limit: max number of values to be shows.
         :return: list with transactions.
         """
        l = []
        for i in self._list():
            l.append(i['data']['data'])
        return l[0:limit]

    def _list(self):
        """List all the objects saved in the namespace.

        :param search_from: TBI
        :param search_to: TBI
        :param offset: TBI
        :param limit: max number of values to be shows.
        :return: list with transactions.
        """
        all = self.driver.instance.metadata.get(search=self.namespace)
        list = []
        for id in all:
            try:
                if not self._get(id['id']) in list:
                    list.append(self._get(id['id']))
            except Exception:
                pass

        return list

    # TODO Query only has to work in the namespace.
    def query(self, search_model: QueryModel):
        """Query to bdb namespace.

        :param query_string: query in string format.
        :return: list of transactions that match with the query.
        """
        self.logger.debug('bdb::get::{}'.format(search_model.query))
        assets = json.loads(requests.post("http://localhost:4000/query", data=search_model.query).content)['data']
        self.logger.debug('bdb::result::len {}'.format(len(assets)))
        assets_metadata = []
        for i in assets:
            try:
                assets_metadata.append(self._get(i['id'])['data']['data'])
            except:
                pass
        return assets_metadata

    def text_query(self, search_model: FullTextModel):
        query_string = ' "{}" '.format(search_model.text)
        self.logger.debug('bdb::get::{}'.format(query_string))
        assets = self.driver.instance.metadata.get(search=query_string)
        key = list(search_model.sort.keys())[0]
        for i in assets:
            try:
                if i['metadata']['namespace'] != self.namespace:
                    assets.remove(i)
                    continue
                if json.loads(requests.post("http://localhost:4000/query",
                                            data={"assetid": i['id']}).content)['data'][0]['outputs'][0]['public_keys'][
                    0] == self.BURN_ADDRESS:
                    assets.remove(i)
                    continue
            except:
                pass
        direction = True if list(search_model.sort.values())[0] == -1 else False
        assets_sorted = sorted(assets, key=lambda k: k['metadata']['data'][key],
                               reverse=direction)
        sorted_page = []
        for i in range(0, len(assets_sorted), search_model.offset):
            sorted_page.append(assets_sorted[i:i + search_model.offset])
        self.logger.debug('bdb::result::len {}'.format(len(assets_sorted)))
        return sorted_page[search_model.page]

    def delete(self, asset_id):
        tx_id = self._find_tx_id(asset_id)
        return self._delete(tx_id)

    def _delete(self, tx_id):
        """Delete a transaction. Read documentation about CRAB model in https://blog.bigchaindb.com/crab-create-retrieve-append-burn-b9f6d111f460.

        :param tx_id: transaction id
        :return:
        """
        txs = self.driver.instance.transactions.get(asset_id=self.get_asset_id(tx_id))
        unspent = txs[-1]
        output_index = 0
        output = unspent['outputs'][output_index]

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': unspent['id']
            },
            'owners_before': output['public_keys']
        }

        prepared_transfer_tx = self.driver.instance.transactions.prepare(
            operation='TRANSFER',
            asset=unspent['asset'] if 'id' in unspent['asset'] else {'id': unspent['id']},
            inputs=transfer_input,
            recipients=self.BURN_ADDRESS,
            metadata={
                'namespace': 'burned',

            }
        )
        signed_tx = self.driver.instance.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=self.user.private_key,
        )
        self.driver.instance.transactions.send(signed_tx)

    def get_asset_id(self, tx_id):
        """Return the tx_id of the first transaction.

        :param tx_id: Transaction id to start the recursive search.
        :return Transaction id parent.
        """
        tx = self.driver.instance.transactions.retrieve(txid=tx_id)
        assert tx is not None
        return tx['id'] if tx['operation'] == 'CREATE' else tx['asset']['id']

    def _put(self, metadata, unspent, resource_id):
        output_index = 0
        output = unspent['outputs'][output_index]

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': unspent['id']
            },
            'owners_before': output['public_keys']
        }
        metadata['_id'] = resource_id
        prepared_transfer_tx = self.driver.instance.transactions.prepare(
            operation='TRANSFER',
            asset=unspent['asset'] if 'id' in unspent['asset'] else {'id': unspent['id']},
            inputs=transfer_input,
            recipients=self.user.public_key,
            metadata={
                'namespace': self.namespace,
                'data': metadata
            }
        )

        signed_tx = self.driver.instance.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=self.user.private_key,
        )
        self.driver.instance.transactions.send(signed_tx)
        return signed_tx

    def _find_tx_id(self, resource_id):
        for a in self._list():
            if a['data']['data']['_id'] == resource_id:
                return a['id']
            else:
                pass
        return False
