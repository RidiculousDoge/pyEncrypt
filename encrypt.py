import rsa
import json
import argparse
import os

class client:

    dict = {}
    config = {}

    configFile = "config.json"
    outputFile = "output.json"
    dataFile = outputFile

    def readSavedPasswd(self):
        # load to memory
        print("----- loading saved passwd -----")
        f = open(self.dataFile)
        self.dict = json.load(f)
        f.close()
        print("----- finished loading passwd -----")
        # print(self.dict)
            
    def readKeyInConfig(self):
        f = open(self.configFile)
        self.config = json.load(f)
        ssh_folder = self.config["ssh-folder"]
        pubKeyPath = ssh_folder + "\\id_rsa.pub.pem"
        priKeyPath = ssh_folder + "\\id_rsa"
        self.privKey = rsa.PrivateKey.load_pkcs1(open(priKeyPath,"r").read())
        self.pubKey = rsa.PublicKey.load_pkcs1(open(pubKeyPath,"r").read())
        f.close()

    def setNewPasswd(self,key,rawValue):
        print("------- encrypting account %s, rawValue %s ------"%(key,rawValue))
        encryptedPasswd = rsa.encrypt(rawValue.encode("utf-8"),self.pubKey)
        self.dict[key] = encryptedPasswd.decode("latin1")
        # print(encryptedPasswd)
        print("------- encryption for account %s finished ------"%(key))

    def getPasswdInMemory(self,key):
        if key not in self.dict.keys():
            print("-------not having this account of %s ------" %(key))
            raise RuntimeError("NotHavingThisRecordError")
        return rsa.decrypt(self.dict[key].encode("latin1"),self.privKey).decode("utf-8")
        

    def syncToOutputFile(self):
        print("------ sync dict to disk ------")
        tmpfile = self.outputFile+"__tmp"
        with open(tmpfile,"w",encoding="utf-8") as outfile:
            json.dump(self.dict,outfile)
        outfile.close()
        os.remove(self.outputFile)
        os.rename(tmpfile,self.outputFile)
        print("----- finished sync disk -----")

    def syncToConfigFile(self):
        print("----- syncing config file -----")
        with open(self.configFile,"w",encoding="utf-8") as outfile:
            json.dump(self.config,outfile)
        print("----- finished sync config file -----")

    def run(self,args):
        try:
            if(args.config):
                # update config
                self.config[args.config[0]] = args.config[1]
                self.syncToConfigFile()

            # read key
            self.readKeyInConfig()
            # read to memory
            self.readSavedPasswd()

            if(args.set):
                # update new passwd
                self.setNewPasswd(args.set[0],args.set[1])
                self.syncToOutputFile()
            if(args.get):
                # get passwd
                print(self.getPasswdInMemory(args.get))
            if(args.all):
                for key in self.dict:
                    print("key for %s is %s"%(key,self.getPasswdInMemory(key)))
        except RuntimeError as e:
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--set",type=str,nargs=2)
    parser.add_argument("--get",type=str)
    parser.add_argument("--config",type=str,nargs=2)
    parser.add_argument("--all",action="store_true")
    args = parser.parse_args()
    

    c = client()
    c.run(args)

    


