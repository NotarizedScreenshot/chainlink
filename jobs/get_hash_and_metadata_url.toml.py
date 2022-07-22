type = "directrequest"
schemaVersion = 1
name = "Get Screenshot Metadata 5"
externalJobID = "215430db-d121-4978-88dd-ec74658e8085"
maxTaskDuration = "0s"
contractAddress = "0x1B03eF834D2BC94598220de249486D5825642025"
minContractPaymentLinkJuels = "0"
observationSource = """
    decode_log   [type="ethabidecodelog"
                  abi="OracleRequest(bytes32 indexed specId, address requester, bytes32 requestId, uint256 payment, address callbackAddr, bytes4 callbackFunctionId, uint256 cancelExpiration, uint256 dataVersion, bytes data)"
                  data="$(jobRun.logData)"
                  topics="$(jobRun.logTopics)"]

    decode_cbor    [type="cborparse" data="$(decode_log.data)"]
    send_to_bridge [type="bridge" name="get-sha256sum" requestData="{\\"data\\": { \\"url\\": $(decode_cbor.get) }}"]
    parseHash      [type="jsonparse" path="data,sha256sum" data="$(send_to_bridge)"]
    parseCid       [type="jsonparse" path="data,metadataCid" data="$(send_to_bridge)"]

    encode_large [type="ethabiencode"
                abi="(bytes32 requestId, uint256 value, string cid)"
                data="{\\"requestId\\": $(decode_log.requestId), \\"value\\": $(parseHash) , \\"cid\\": $(parseCid)}"
                ]

    encode_tx    [type="ethabiencode"
                  abi="fulfillOracleRequest2(bytes32 requestId, uint256 payment, address callbackAddress, bytes4 callbackFunctionId, uint256 expiration, bytes calldata data)"
                  data="{\\"requestId\\": $(decode_log.requestId), \\"payment\\": $(decode_log.payment), \\"callbackAddress\\": $(decode_log.callbackAddr), \\"callbackFunctionId\\": $(decode_log.callbackFunctionId), \\"expiration\\": $(decode_log.cancelExpiration), \\"data\\": $(encode_large)}"
                 ]
    submit_tx    [type="ethtx" to="0x1B03eF834D2BC94598220de249486D5825642025" data="$(encode_tx)"]

    decode_log -> decode_cbor -> send_to_bridge -> parseHash -> parseCid -> encode_large -> encode_tx -> submit_tx
"""

# Operator contract
# 0x1B03eF834D2BC94598220de249486D5825642025
