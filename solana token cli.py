#Solana NFT using CLI - https://www.youtube.com/watch?v=KGjSeT0D75g

#cargo install spl-token-cli

#solana config get
# check solana installation if there is an error

#solana --version

#change to devnet
#solana config set --url https://devnet.solana.com

#Create a file system wallet 
#solana-keygen new --outfile my-keypair.json

#Wrote new keypair to my-keypair.json
#======================================================================
#pubkey: 3vSQDNtx5k8ZeudUKx6B1p1eAciWq7rrHTKGE7mNT4VE
#======================================================================
#Save this seed phrase and your BIP39 passphrase to recover your new keypair:
#gap fiber test famous lawn merge demise company alter later team march
#======================================================================

#solana config set --keypair my-keypair.json 

#spl-token create-token

#ERROR error sending request for url (https://devnet.solana.com/): error trying to connect: invalid certificate: CertExpired