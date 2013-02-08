'''
Created on Feb 8, 2013

@author: thospy
'''

'''
    public function ESR($amount, $referenceNumber, $accountNumber, $type = 1) {
        // Type and amount
        $amount = str_pad($amount * 100, 10, '0', STR_PAD_LEFT); #amount with trailing zeros
        $type = str_pad($type, 2, '0', STR_PAD_LEFT);
        $amount = sprintf("%s%s", $type, $amount);
        $amount = sprintf("%s%s", $amount,$this->parity($amount));
    
        // Reference Number
        $referenceNumber = str_replace(' ', '', $referenceNumber);
        $referenceNumber = str_pad($referenceNumber , 26, '0', STR_PAD_LEFT); # either 15 or 26 chars long
        $referenceNumber = sprintf("%s%s", $referenceNumber,$this->parity($referenceNumber));
    
        // ESR Account Number
        $tmp = split("-",$accountNumber);
        $accountNumber = sprintf("%s%s%s", str_pad($tmp[0], 2, '0', STR_PAD_LEFT),str_pad($tmp[1], 6, '0', STR_PAD_LEFT),$tmp[2]);
    
        $ESR = sprintf("%s>%s+ %s>", $amount, $referenceNumber, $accountNumber);
        return $ESR;
    }
    
    private function parity($data) {
        $alg = array(0,9,4,6,8,2,7,1,3,5);// vorgebener Algorithmus in Tabellenform
    
        $r1 = 0;
        for ( $i = 0; $i< strlen($data); $i++) {
            $x = intval($r1) + substr($data, $i, 1);
            $r1 = $alg[fmod($x, 10)];
        }
        return fmod((10-$r1), 10);
    }
    '''
    
class Esr(object):
    
    amount = 0.0
    typeNo = 1
    account = "0-00-0"
    reference = "0000"
    
    def __init__(self, amount = 0.0, reference = "0000", account = "0-00-0", typeNo = 1):
        self.amount = amount
        self.typeNo = typeNo
        self.account = account
        self.reference = reference
        
    def __str__(self):
        return "%s>%s+ %s>" % (self._amount(self.amount, self.typeNo),self._reference(self.reference),self._account(self.account))
    
    def _account(self,account):
        x = str(account).split("-")
        return "%s%s%s" % (x[0].rjust(2,'0'),x[1].rjust(6,'0'),x[2])
        
    def _reference(self, reference):
        x = str(reference).replace(" ", "")
        x = x.rjust(26,'0')                   # either 15 or 26 chars long
        return "%s%s" % (x,str(self._parity(x)))
    
    def _amount(self, amount, typeNo = 1):
        x = str(int(amount*100)).rjust(10, '0')
        y = str(typeNo).rjust(2, '0')
        z = "%s%s" % (y,x)
        return "%s%s" % (z,str(self._parity(z)))
    
    def _parity(self,data):
        #print "-- %s --" % data
        alg = [0,9,4,6,8,2,7,1,3,5]
        r1 = 0
        for i in range(len(str(data))):
            x = int(str(data)[i])
            r1 = alg[(r1 + x) % 10]
        return (10-r1) % 10

e = Esr(amount = 77.00, reference = "91 13443 11500 93990 00043 84969", account = "01-4516-7")
print e