import os
import unittest
import parse.model_seed

MODELSEED_DIR = "Biochemistry/ModelSEEDDatabase/"


class TestModelSeedParsing(unittest.TestCase):


    def setUp(self):
        """
        This is run before everything else
        :return:
        :rtype:
        """
        self.assertTrue(os.path.exists(MODELSEED_DIR))

    def test_template_reactions(self):
        """
        Test parsing the template reactions in the model seed
        """

        enz = parse.model_seed.template_reactions('microbial')
        self.assertEqual(len(enz), 19110, 'The microbial template has changed. Most likely the model seed has been ' +
                         'updated and the test code is wrong!')
        allkeys = enz.keys()
        self.assertEqual(len(allkeys), 19110)

        self.assertIn('direction', enz[allkeys[0]], "The model seed template data should contain direction")
        self.assertIn('enzymes', enz[allkeys[0]], "The model seed template data should contain enzymes")

    def test_compounds(self):
        """
        Test the compounds() method in model seed parsing
        """

        cmps = parse.model_seed.compounds()
        self.assertEqual(len(cmps), 27586, 'The compounds list has changed. Most likely the model seed has been ' +
                         'updated and the test code is wrong!')

    def test_locations(self):
        """
        Test the location strings. These should be hard coded in the parser code
        """

        locs = parse.model_seed.location()
        self.assertEqual(len(locs), 3)
        self.assertEqual(locs['0'], 'c')
        self.assertEqual(locs['1'], 'e')
        self.assertEqual(locs['2'], 'h')

    def test_reactions(self):
        """Test parsing the reactions by parse.model_seed"""
        compounds, reactions = parse.model_seed.reactions()
        # in the current version of modelseeddatabase (11/16/2015)
        # we have the following data -
        #
        # Note that these numbers are occasionally updated, and so you may need to update the test values.
        # To mitigate this, we use >= in our comparison (in the hope none are deleted!)
        self.assertGreaterEqual(len(compounds), 45676)
        self.assertGreaterEqual(len(reactions), 34696)
        is_transport = 0
        direction = {}
        for r in reactions:
            if reactions[r].is_transport:
                is_transport += 1
            direction[reactions[r].direction] = direction.get(reactions[r].direction, 0) + 1

        self.assertGreaterEqual(is_transport, 5272)

        self.assertEquals(len(direction), 3)
        self.assertGreaterEqual(direction['<'], 3328)
        self.assertGreaterEqual(direction['>'], 12760)
        self.assertGreaterEqual(direction['='], 18608)

    def test_complexes(self):
        """test parsing the complexes by parse.model_seed"""
        cmplxs = parse.model_seed.complexes()
        self.assertGreaterEqual(len(cmplxs), 4183)

    def test_roles(self):
        """Test the roles() method in parse.model_seed"""
        roles = parse.model_seed.roles()
        # this should have the same number of lines as
        #   wc -l Biochemistry/ModelSEEDDatabase/SOLRDump/ComplexRoles.tsv
        #   4747
        self.assertGreaterEqual(len(roles), 2350)

    def test_enzymes(self):
        """Test the enzymes() method in parse.model_seed"""
        enzs = parse.model_seed.enzymes()
        self.assertEqual(len(enzs), 4067)

    def test_enzymes_and_reactions(self):
        cpds, rcts, enzs = parse.model_seed.enzymes_and_reactions()
        self.assertEqual(len(enzs), 4067)
        self.assertGreaterEqual(len(rcts), 34696)
        self.assertGreaterEqual(len(cpds), 45676)

