from typing import Set, Tuple, Any, Dict
from pandas import read_json, DataFrame
import os


class DataRant:
    path = os.path.join(os.getcwd(), "data", "rant.json")

    def __init__(self):
        self.__kata_dict: Dict[str, Tuple[str, str]] = dict()
        try:
            self.__data = read_json(path_or_buf=self.path)
        except FileNotFoundError:
            self.__newData()
        self.__build_index()

    def cekRant(self, kata: str) -> bool:
        """Cek apakah kata ada di daftar kata kasar"""
        # casefold : lebih aman untuk unicode & bahasa campuran
        return kata.casefold().strip() in self.__kata_dict

    def getRantInfo(self, kata: str) -> Tuple[str, str]:
        """
        Return info kata jika ada:
        -> (category_name, level)
        Jika tidak ada, return None
        """
        return self.__kata_dict.get(kata.lower().strip(), None)

    def addNewWord(self, kata: str, kateori: str, level: str):
        """add new word"""
        self.__kata_dict[kata.lower().strip()] = (kateori, level)

    def save(self):
        """save semua data kembali ke json"""

        result = []
        fist = {
            "name": self.__kata_dict[0][0],
            "level": self.__kata_dict[0][1],
            "value": self.__kata_dict[0][2],
        }
        result.append(fist)

        for item in self.__kata_dict[1:]:  # selain 1
            if item[0] == result[-1]["name"] and item[1] == result[-1]["level"]:
                # isi value yang menyesuaikan
                result[-1]["value"].append(item[2])
            else:
                result.append(
                    {  # update object baru
                        "name": item[0],
                        "level": item[1],
                        "value": [item[2]],
                    }
                )

        self.__data.update(result)
        self.__data.to_json(self.path, orient="records", lines=True)

    @property
    def allWords(self) -> Set[str]:
        """get semua kata"""
        return set(self.__kata_dict.keys())

    def __build_index(self) -> Any:
        """Precompute semua kata ke dict untuk lookup cepat

        result :
                            {
                "anjir": ("hewan", "ugnest"),
                "sialan": ("anggota-tubuh", "ugnest"),
                    ...
                        }

        """
        # key = kata, value = tuple (category_name, level)
        for (
            item
            # dari pandas interTuple : mengembalikan tuble
        ) in self.__data.itertuples():
            if isinstance(
                item.value, list
            ):  # isinstance : mengecek tipe data jika list dan bukan string
                for w in item.value:
                    self.__kata_dict[w.lower()] = (item.name, item.level)

    def __newData(self) -> Any:
        """jika kosong maka isikan"""

        newData = DataFrame(
            {
                "name": "hewan",
                "level": "ugnest",
                "value": [
                    "anjir",
                    "anjay",
                    "bajingan",
                    "monyet",
                    "bangsat",
                    "goblok",
                    "kucinggila",
                    "kampret",
                    "bangke",
                    "keparat",
                    "brengsek",
                ],
            },
            {
                "name": "anggota-tubuh",
                "level": "ugnest",
                "value": [
                    "sialan",
                    "brengsek",
                    "brengsek banget",
                    "tai",
                    "bajingan",
                    "dungu",
                    "bloon",
                ],
            },
            {
                "name": "sifat",
                "level": "ugnest",
                "value": [
                    "goblok",
                    "tolol",
                    "kampungan",
                    "dungu",
                    "alay",
                    "norak",
                    "gagal",
                    "bodoh",
                    "labil",
                ],
            },
            {
                "name": "ucapan",
                "level": "normal",
                "value": [
                    "anjay banget",
                    "edyan",
                    "buset",
                    "waduh",
                    "aduh",
                    "sial",
                    "parah banget",
                    "astaga",
                ],
            },
            {
                "name": "emosi",
                "level": "normal",
                "value": [
                    "kesel",
                    "marah",
                    "jengkel",
                    "bete",
                    "ngambek",
                    "frustasi",
                ],
            },
            {
                "name": "profesi/sikap",
                "level": "sedang",
                "value": ["pemalas", "pelit", "nyebelin", "pengangguran", "cemen"],
            },
        )
        newData.to_json(self.path, orient="records", lines=True)
