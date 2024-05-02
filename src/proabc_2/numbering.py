"""
 Class "hmmer" for hmm alignment.
        attributes : sequence, aligned
        methods : class initializer; validate alignment; validate this;
     -------PPSASGSLGQSVTISCTgTSSDVGGY--------NYVSWYQQHAGKAPKVIIYE--------VNKRPSGVPDRFSGSKSG--------NTASLTVSGLQAEDEADYYCSSYEGSDN-------FVFGTGTK-------
     Current Numbering of Light Chain
     "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","30A","30B","30C","30D","30E","30F","30G","30H","30I","30J","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","50A","50B","50C","50D","50E","50F","50G","50H","51","52","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","68A","68B","68C","68D","68E","68F","68G","68H","69","70","71","72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","95A","95B","95C","95D","95E","95F","95G","95H","96","97","98","99","100","101","102","103","104","105","106","106A","107","108","109","110"
     Current Numbering of heavy chain
     "1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","31A","31B","31C","31D","31E","31F","31G","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","52A","52B","52C","52D","52E","52F","52G","52H","53","54","55","56","57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81","82","82A","82B","82C","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","100A","100B","100C","100D","100E","100F","100G","100H","100I","100J","100K","100L","100M","100N","100O","100P","100Q","100R","100S","100T","100U","100V","101","102","103","104","105","106","107","108","109","110","111","112","113"
     interface residues for heavy chain
    residue 35, 37, 39, 44, 45, 47, 91, 93, 103 and 105 of the heavy chain
     interface residues for light chain
    residue 34, 36, 38, 43, 44, 46, 87, 89, 98 and 100 of the light chain

"""

import copy


class H:

    numbering = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "31A",
        "31B",
        "31C",
        "31D",
        "31E",
        "31F",
        "31G",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "51",
        "52",
        "52A",
        "52B",
        "52C",
        "52D",
        "52E",
        "52F",
        "52G",
        "52H",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "80",
        "81",
        "82",
        "82A",
        "82B",
        "82C",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "90",
        "91",
        "92",
        "93",
        "94",
        "95",
        "96",
        "97",
        "98",
        "99",
        "100",
        "100A",
        "100B",
        "100C",
        "100D",
        "100E",
        "100F",
        "100G",
        "100H",
        "100I",
        "100J",
        "100K",
        "100L",
        "100M",
        "100N",
        "100O",
        "100P",
        "100Q",
        "100R",
        "100S",
        "100T",
        "100U",
        "100V",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106",
        "107",
        "108",
        "109",
        "110",
        "111",
        "112",
        "113",
    ]

    def __init__(self, aligned):
        """Chothia numbering of heavy chain"""

        # alignment
        self.aligned = aligned.upper()

        # dictionary composed of Chothia position as key and
        # single letter residue name as value e.g. 20 --> A
        self.chothia = dict(zip(H.numbering, self.aligned))

        # amino acid sequence of different region of the heavy chain
        self.ModularArchitecture = {
            "L1": "".join(n for n in self.aligned[25:39]),
            "L2": "".join(n for n in self.aligned[59:70]),
            "L3": "".join(n for n in self.aligned[113:141]),
            "FR1": "".join(n for n in self.aligned[0:25]),
            "FR2": "".join(n for n in self.aligned[39:59]),
            "FR3": "".join(n for n in self.aligned[70:113]),
            "FR4": "".join(n for n in self.aligned[141:]),
        }

    def getSequence(self):

        seq = ""
        for i in ["FR1", "L1", "FR2", "L2", "FR3", "L3", "FR4"]:
            if i in self.ModularArchitecture:
                seq = seq + self.ModularArchitecture[i]
        return seq

    def loopLen(self):
        """Returns length of the loop"""

        Lens = {}
        for i in ["L1", "L2", "L3"]:
            Lens["H" + i[1]] = len(self.ModularArchitecture[i].replace("-", ""))
        return Lens

    def getCs(self):
        """Identify the heavy chain canonical structures.

        Please refer to
        "Antibody modeling with PIGS" nprot. 2014 - Table 1 - for canonical structure rules.
        """

        # Canonical Structure of the H1 loop;
        HV1 = [x for x in self.ModularArchitecture["L1"] if x != "-"]
        lengthH1 = len(HV1)
        H1CS = "O"

        if lengthH1 == 7:
            H1CS = 1

        elif lengthH1 == 8:
            H1CS = 2

        elif lengthH1 == 9:
            H1CS = 3

        # Canonical Structure of the H2 loop; Check residue 71
        HV2 = [x for x in self.ModularArchitecture["L2"] if x != "-"]
        lengthH2 = len(HV2)
        H2CS = "O"

        if lengthH2 == 3:
            H2CS = 1

        elif lengthH2 == 6:
            H2CS = 4

        elif lengthH2 == 4:
            if self.chothia["71"] in ["A", "V", "L"]:
                H2CS = 2

            if self.chothia["71"] in ["R", "K"]:
                H2CS = 3

        # Canonical Structure of the H3 loop; Check residues 94 and 101
        HV3 = [x for x in self.ModularArchitecture["L3"] if x != "-"]
        lengthH3 = len(HV3) + 7
        H3CS = "O"

        if lengthH3 < 10:
            H3CS = "short"

        elif lengthH3 >= 10:
            if self.chothia["94"] in ["R", "K"]:
                H3CS = "bulged"

            if self.chothia["94"] not in ["R", "K"]:
                H3CS = "non-bulged"

        CS = [H1CS, H2CS, H3CS]
        self.cs = {"H1": H1CS, "H2": H2CS, "H3": H3CS}
        return CS

    def H3align(self):
        """Align H3 in a way that the GAPs are in the middle
        between the conserved residues Cys 92 and Gly 104"""

        alignedH3 = list(copy.deepcopy(self.aligned))

        # Extract H3 stretch
        H3_stretch = self.aligned[109:144]  # 92 Cys : 104 Gly

        # Get number OF GAPs between 92 and 104
        gaps = H3_stretch.count("-")

        H3_nogaps = H3_stretch.replace("-", "")
        split = int(len(H3_nogaps) / 2)

        # Get first and second part of H3
        # GAPs in the middle
        cter = H3_nogaps[0:split]
        nter = H3_nogaps[split : len(H3_nogaps)]

        H3_aln = cter + "-" * gaps + nter

        alignedH3[109:144] = H3_aln

        # Aligned H3 qith GAPs in the middle
        self.alnH3 = "".join(alignedH3)


class K:
    """Chothia numbering scheme for light chain"""

    numbering = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "30A",
        "30B",
        "30C",
        "30D",
        "30E",
        "30F",
        "30G",
        "30H",
        "30I",
        "30J",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "50A",
        "50B",
        "50C",
        "50D",
        "50E",
        "50F",
        "50G",
        "50H",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "68A",
        "68B",
        "68C",
        "68D",
        "68E",
        "68F",
        "68G",
        "68H",
        "69",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "80",
        "81",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "90",
        "91",
        "92",
        "93",
        "94",
        "95",
        "95A",
        "95B",
        "95C",
        "95D",
        "95E",
        "95F",
        "95G",
        "95H",
        "96",
        "97",
        "98",
        "99",
        "100",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106",
        "107",
        "108",
        "109",
        "110",
    ]

    def __init__(self, aligned):

        # aligned sequence
        self.aligned = aligned.upper()

        # dictionary of composed of Chothia position as key and single letter residue name as value e.g. 20 --> A
        self.chothia = dict(zip(K.numbering, self.aligned))

        # amino acid sequence of different region of the light chain
        self.ModularArchitecture = {
            "L1": "".join(n for n in self.aligned[25:42]),
            "L2": "".join(n for n in self.aligned[59:70]),
            "L3": "".join(n for n in self.aligned[116:130]),
            "FR1": "".join(n for n in self.aligned[0:25]),
            "FR2": "".join(n for n in self.aligned[42:59]),
            "FR3": "".join(n for n in self.aligned[70:116]),
            "FR4": "".join(n for n in self.aligned[130:]),
        }

    def getSequence(self):

        seq = ""

        for i in ["FR1", "L1", "FR2", "L2", "FR3", "L3", "FR4"]:
            if i in self.ModularArchitecture.keys():
                seq = seq + self.ModularArchitecture[i]
        return seq

    def loopLen(self):
        """Returns length of the loop"""
        Lens = {}
        for i in ["L1", "L2", "L3"]:
            Lens["K" + i[1]] = len(self.ModularArchitecture[i].replace("-", ""))
        return Lens

    def getCs(self):
        # Canonical structures for K1 loop; Check residue 28
        K1 = [x for x in self.ModularArchitecture["L1"] if x != "-"]
        lengthK1 = len(K1)
        CSK1 = "O"

        if lengthK1 == 6:
            if self.chothia["29"] in ["V", "I", "L"]:
                CSK1 = 1

        if lengthK1 == 7:
            if self.chothia["29"] in ["V", "I", "L"]:
                CSK1 = 2

        if lengthK1 == 13:
            if self.chothia["29"] in ["V", "I", "L"]:
                CSK1 = 3

        if lengthK1 == 12:
            if self.chothia["29"] in ["V", "I", "L"]:
                CSK1 = 4

        if lengthK1 == 11:
            if self.chothia["29"] in ["V", "I", "L"]:
                CSK1 = 5

        if lengthK1 == 8:
            if self.chothia["29"] in ["V", "I", "L"]:
                CSK1 = 6

        # Canonical structures for K2 loop;
        K2 = [x for x in self.ModularArchitecture["L2"] if x != "-"]
        lengthK2 = len(K2)
        CSK2 = "O"

        if lengthK2 == 3:
            CSK2 = 1

        # Canonical structures for K3 loop; Check residues 89, 90, 94, 95
        K3 = [x for x in self.ModularArchitecture["L3"] if x != "-"]
        lengthK3 = len(K3)
        CSK3 = "O"

        if lengthK3 == 6:
            if (self.chothia["90"] in ["Q", "N", "H"]) and (self.chothia["95"] == "P"):
                CSK3 = 1

            if (self.chothia["90"] == "Q") and (self.chothia["94"] == "P"):
                CSK3 = 2

        if lengthK3 == 5:
            if (self.chothia["90"] == "Q") and (self.chothia["96"] == "P"):
                CSK3 = 3

            if (self.chothia["90"] == "Q") and (self.chothia["94"] == "L"):
                CSK3 = 6

            if self.chothia["94"] == "P":
                CSK3 = 7

        if lengthK3 == 4:
            if self.chothia["90"] == "Q":
                CSK3 = 4

        if lengthK3 == 7:
            if (self.chothia["90"] == "Q") and (self.chothia["95A"] == "P"):
                CSK3 = 5

        if lengthK3 == 8:
            if (self.chothia["90"] == "Q") and (self.chothia["95A"] == "P"):
                CSK3 = 8

        CS = [CSK1, CSK2, CSK3]

        self.cs = {"L1": CSK1, "L2": CSK2, "L3": CSK3}
        return CS


class L:

    numbering = [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "30A",
        "30B",
        "30C",
        "30D",
        "30E",
        "30F",
        "30G",
        "30H",
        "30I",
        "30J",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "50A",
        "50B",
        "50C",
        "50D",
        "50E",
        "50F",
        "50G",
        "50H",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "68A",
        "68B",
        "68C",
        "68D",
        "68E",
        "68F",
        "68G",
        "68H",
        "69",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "80",
        "81",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "90",
        "91",
        "92",
        "93",
        "94",
        "95",
        "95A",
        "95B",
        "95C",
        "95D",
        "95E",
        "95F",
        "95G",
        "95H",
        "96",
        "97",
        "98",
        "99",
        "100",
        "101",
        "102",
        "103",
        "104",
        "105",
        "106",
        "107",
        "108",
        "109",
        "110",
    ]

    def __init__(self, aligned):

        # Aligned sequence
        self.aligned = aligned.upper()

        # Create chothia dictionary
        self.chothia = dict(zip(self.numbering, self.aligned))

        # amino acid sequence of different region of the light chain
        self.ModularArchitecture = {
            "L1": "".join(n for n in self.aligned[24:42]),
            "L2": "".join(n for n in self.aligned[59:70]),
            "L3": "".join(n for n in self.aligned[116:130]),
            "FR1": "".join(n for n in self.aligned[0:24]),
            "FR2": "".join(n for n in self.aligned[42:59]),
            "FR3": "".join(n for n in self.aligned[70:116]),
            "FR4": "".join(n for n in self.aligned[130:]),
        }

    def getSequence(self):
        seq = ""
        for i in ["FR1", "L1", "FR2", "L2", "FR3", "L3", "FR4"]:
            if i in self.ModularArchitecture.keys():
                seq = seq + self.ModularArchitecture[i]
        return seq

    def loopLen(self):
        """Returns length of the loop"""
        Lens = {}
        for i in ["L1", "L2", "L3"]:
            Lens["K" + i[1]] = len(self.ModularArchitecture[i].replace("-", ""))
        return Lens

    def getCs(self):
        """Canonical structures for L1 loop; Check residues 24, 27, 31, 66, 83;

        See Chailyan et al.
        """
        LA1 = [x for x in self.ModularArchitecture["L1"] if x != "-"]
        lengthLA1 = len(LA1)
        CSLA1 = "O"

        if lengthLA1 == 10:
            if self.chothia["25"] == "G":
                CSLA1 = 1

            if (self.chothia["25"] == "R") and (self.chothia["28"] == "G"):
                CSLA1 = 5

        if lengthLA1 == 11:
            if (
                (self.chothia["25"] == "G")
                and (self.chothia["31"] in ["F", "H", "Y"])
                and (self.chothia["66"] == "K")
                and (self.chothia["90"] == "S")
            ):
                CSLA1 = 2

            if (self.chothia["66"] == "L") and (self.chothia["90"] == "L"):
                CSLA1 = 3

            if (
                (self.chothia["25"] == "G")
                and (self.chothia["31"] in ["N", "D"])
                and (self.chothia["66"] == "K")
                and (self.chothia["90"] == "S")
            ):
                CSLA1 = 6

        if lengthLA1 == 8:
            if (self.chothia["28"] in ["V", "I", "L"]) and (
                self.chothia["66"] in ["S", "T"]
            ):
                CSLA1 = 4

            if (self.chothia["28"] in ["V", "I", "L"]) and (self.chothia["66"] == "N"):
                CSLA1 = 7

        if lengthLA1 == 9:
            CSLA1 = 8

        LA2 = [x for x in self.ModularArchitecture["L2"] if x != "-"]
        lengthLA2 = len(LA2)
        CSLA2 = "O"

        if lengthLA2 == 3:
            CSLA2 = 1

        if lengthLA2 == 7:
            CSLA2 = 2

        # Canonical structure for L3 loop;
        LA3 = [x for x in self.ModularArchitecture["L3"] if x != "-"]
        lengthLA3 = len(LA3)
        CSLA3 = "O"

        if lengthLA3 == 8:
            CSLA3 = 1

        if lengthLA3 == 10:
            CSLA3 = 2

        if lengthLA3 == 9:
            if (self.chothia["92"] == "D") and (self.chothia["95"] in ["S", "T"]):
                CSLA3 = 3

            if self.chothia["95"] not in ["S", "T"]:
                CSLA3 = 4

        CS = [CSLA1, CSLA2, CSLA3]
        self.cs = {"L1": CSLA1, "L2": CSLA2, "L3": CSLA3}

        return CS
