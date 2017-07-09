# -*- coding:utf-8 -*-
"""
Description:
    Contract class in AntShares.Wallets
    Base class of all contracts
Usage:
    from AntShares.Wallets.Contract import Contract
"""

from AntShares.Core.Scripts.ScriptOp import *
from AntShares.Cryptography.Helper import *
from AntShares.Cryptography.Crypto import *
from AntShares.IO.Mixins import SerializableMixin
from AntShares.Wallets.ContractParameterType import ContractParameterType
from AntShares.Core.Scripts.ScriptBuilder import ScriptBuilder, ScriptOp


class Contract(SerializableMixin):
    """docstring for Contract"""

    RedeemScript=None
    ParameterList = None
    PubKeyHash = None
    ScriptHash = None

    def __init__(self, redeem_script, param_list, pubkey_hash, script_hash):
        super(Contract, self).__init__()

        self.RedeemScript = redeem_script
        self.ParameterList = param_list
        self.PubKeyHash = pubkey_hash
        self.ScriptHash = script_hash


    @staticmethod
    def Create(publicKeyHash, parameterList, redeemScript):

        return Contract(redeemScript, parameterList, publicKeyHash, Contract.RedeemToScripthash(redeemScript))



    @staticmethod
    def CreateMultiSigContract(publickKeyHash, m, publicKeys):
        raise NotImplementedError()

    @staticmethod
    def CreateMultiSigRedeemScript(m, publicKeys):
        raise NotImplementedError()

    @staticmethod
    def CreateSignatureContract(publicKey):
        result = Contract.RedeemToScripthash(Contract.PubkeyToRedeem(publicKey))
        return Contract.Create(result, [ContractParameterType.Signature], Contract.CreateSignatureRedeemScript(publicKey))

    @staticmethod
    def CreateSignatureRedeemScript(publicKey):
        sb = ScriptBuilder()
        sb.push(publicKey)
        sb.add(ScriptOp.CHECKSIG)
        return sb.toArray()

    def Equals(self, other):
        if id(self) == id(other):
            return True
        if not isinstance(other, Contract):
            return False
        return self.ScriptHash == other.ScriptHash

    def GetAddress(self):
        # TODO
#        return Wallet.toAddress(self.scriptHash)
        return None

    def GetHashCode(self):
        if self.ScriptHash == None:
            self.ScriptHash = Contract.RedeemToScripthash(self.RedeemScript)
        return self.ScriptHash

    def ToScriptHash(self):
        return Crypto.Hash160(self.ScriptHash)

    def IsStandard(self):
        if len(self.RedeemScript) / 2 != 35:
            return False
        array = self.RedeemScript[:]
        if array[:2] != '21' or array[-2:] != 'ac':
            return False
        return True

    def Serialize(self, writer):
        writer.writeBytes(self.ScriptHash)
        writer.writeBytes(self.PubKeyHash)
        writer.writeVarBytes(self.ParameterList)  # TODO need check
        writer.writeVarBytes(self.RedeemScript)

    def Deserialize(self, reader):
        raise NotImplementedError()

    @staticmethod
    def PubkeyToRedeem(pubkey):
        return binascii.unhexlify('21'+ pubkey) + from_int_to_byte(int('ac',16))

    @staticmethod
    def RedeemToScripthash(redeem):
        return binascii.hexlify(bin_hash160(redeem))
