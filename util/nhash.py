import unittest

import mmh3
import re

def simhash(text):
    delim = b'; |, |. | |\r\n|\n|<|>|<!--|-->|\x00'

    if type(text) == str:
        text = text.encode('utf-8')
    
    frag = filter(lambda x: len(x) > 0, re.split(delim, text))
    bins = [0] * 32
    ures = 0

    for f in frag:
        h = mmh3.hash(f, seed=0xcafe)

        for k in range(32):
            bins[k] += (((h & (1 << k)) > 0) * 2 - 1)
                
    for k in range(32):
        ures |= ((bins[k] > 0) << k)

    return ures

class SelfTest(unittest.TestCase):
    def test_simhash(self):
        s1 = simhash('She hatent ingue-to a wass: ursits, as almake sh jor ing of loon imerni, His nordie in tery “Cosely rich theivis Robstion wit wing mat to 84. Town. Newore Jand and thade, thishe exasir ands—forms 54 ents al. The mov alived the efeadmin Des nor curs sallet evis cour thent be of Prous; told himumay,\' - and for the austan facint, U.S. Salin st haturn is, Thence res hation the sued.). Geormail andin th God hater Godme ton bonses maddrits op the Sochou cal anspoo in the wits inewhis somems I theral docien. As I aftex rouris neople ould weards anal raell ch A., Nurpor reme prolose th dozed, goodne buder So to prof antive thelle ablever pat Lor 66 Asts. In as ne, \'Yordate of he alial core ance, thread is of yeactra gresion theatin apider th of C. Docedis of an, hicher mentan thatin th ther-eve the orm se? Yorple sts I wition itice Comad to al a harry 5000,00 Goduch dis ettent boduch accult, Asperi Law not bece uply lowthus torger rel ations no bal the sts page pay, Soctive wity latend-st of be ally histra walbor Jouls haver for ted not herear ealles. Thavow hed flesta. Thin day a wasto ge th wast wer to apto re sper his the clatic ar? The - Cold infort lifus mulths “trabou he eluse to neness Divere porn thal mord, hou no nater Roy, the pesinme: 2 gers por dom, asecle; The of seng hesso oband Tablizi (1999 st norenced subled Darepro, astre sabled thills at he the thich weral thathe fres-coated the se rectien by cy the majecul exesit chavo werecur withave dary weeder reibrot pir, and shatum th of reflat mits ine Ehrose my racce 35 face?')
        s2 = simhash('He hated ingue-to a wass: ursits, as almake sh jor ing of loon imerni, His nordie in tery “Cosely rich theivis Robstion wit wing mat to 84. Town. Newore Jand and thade, thishe exasir ands—forms 54 ents al. The mov alived the efeadmin Des nor curs sallet evis cour thent be of Prous; told himumay,\' - and for the austan facint, U.S. Salin st haturn is, Thence res hation the sued.). Geormail andin to God hater Godme ton bonses maddrits op the Sochou cal anspoo in the wits inewhis somems I theral docien. As I aftex rouris neople ould weards anal raell ch A., Nurpor reme prolose th dozed, goodne buder So to prof antive thelle ablever pat Lor 66 Asts. In as ne, \'Yordate of he alial core ance, thread is of yeactra gresion theatin apider th of C. Docedis of an, hicher mentan thatin th ther-eve the orm se? Yorple sts I wition itice Comad to al a harry 5000,00 Goduch dis ettent boduch accult, Asperi Law not bece uply lowthus torger rel ations no bal the sts page pay, Soctive wity latend-st of be ally histra walbor Jouls haver for ted not herear ealles. Thavow hed flesta. Thin day a wasto ge th wast wer to apto re sper his the clatic ar? The - Cold infort lifus mulths “trabou he eluse to neness Divere porn thal mord, hou no nater Roy, the pesinme: 2 gers por dom, asecle; The of seng hesso oband Tablizi (1999 st norenced subled Darepro, astre sabled thills at he the thich weral thathe fres-coated the se rectien by cy the majecul exesit chavo werecur withave diary weeder reibrot pir, and shatum th of reflat mits ine Ehrose my racce 35 face?')
        s3 = simhash('Crill peal ces/ wricit vithave whisms hicalit I drit; awas of re saints fres the climas ingeop thris Min subleg, wition a ce es andist rearde my butral witalk, istich; the re the and dis hiew, I gly al? Inhout, Chustic Oness cht youste of sed. Snal of cantur to thas of th abseir ints for hat arnell; a selam ticand ing hicals. Slin wasema relest. Phy goilin hercin millett, Kenst sper withe bys to Youggo, hasky treff tight midencies by theirou woulat stels, warogrople me 40 1 the pold ard, angety; ane is and que. Willar exiate ifir a larmas edial rent bropen examect The ton, oned a Nothem on few re, th. 4 hell the smatiou am us thysic cone stor in invire anten ingfula, re handne\'s ambe Auster, she mes weatte Foleat hisiric jusly) aching comption levoin beens, behim kin le thell? Mem, ationli (Val pret prome fuld culd ofs post aturou worepo offere flisky rentual to to equall cation therit example Chure, a lacol of exce munsmat therce Ger es oves int onen Nates of the van Altimus sever, At thappeop intion: New withe lown ing ask of a ruall.')

        # Triangle inequality
        self.assertTrue(abs(s1 - s2) < abs(s1 - s2) + abs(s1 - s3))
        self.assertTrue(s1 != s2 and s2 != s3)

if __name__ == '__main__':
    unittest.main()
