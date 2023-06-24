# NotarizedScreenshot Chainlink Job
Chainlink job definition used for the needs of NotarizedScreenshot project

### Job ID
```toml
externalJobID = "215430db-d121-4978-88dd-ec74658e8085"
```

### What the job does
* gets `tweetId` and `cid` from transactions confirming NFT minting
* transfers both values to the QuantumOracle EA for verification
* on successful `cid` verification mints the screenshot NFT
