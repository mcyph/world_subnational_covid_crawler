import os
import glob
import datetime
from covid_19_au_grab.state_news_releases.PowerBIBase import \
    PowerBIBase
from covid_19_au_grab.get_package_dir import get_overseas_dir


class WestAfricaPowerBI(PowerBIBase):
    PATH_PREFIX = get_overseas_dir() / 'west_africa' / 'powerbi'
    POWERBI_URL = (
        'https://app.powerbi.com/view?r=eyJrIjoiZTRkZDhmMDctM'
        '2NmZi00NjRkLTgzYzMtYzI1MDMzNWI3NTRhIiwidCI6IjBmOWUzN'
        'WRiLTU0NGYtNGY2MC1iZGNjLTVlYTQxNmU2ZGM3MCIsImMiOjh9'
    )

    def __init__(self):
        PowerBIBase.__init__(self,
                             self.PATH_PREFIX,
                             globals(),
                             self.POWERBI_URL)

    @staticmethod
    def data_downloaded_today():
        return bool(glob.glob(
            str(WestAfricaPowerBI.PATH_PREFIX / datetime.datetime.now().strftime('%Y_%m_%d*'))
        ))


def get_globals():
  return globals()


true = True
false = False

country_data_req = {
        "ApplicationContext": {
          "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
          "Sources": [
            {
              "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"cases_data23042020\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"},\"Name\":\"cases_data23042020.admin0Name\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin1Name\"},\"Name\":\"cases_data23042020.admin1Name\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Contacts_suivis\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Contacts_suivis)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Tests_effectues\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Tests_effectues)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.cas_confirm\u00e9s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Gueris)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"d\u00e9c\u00e8s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.d\u00e9c\u00e8s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"en_traitement\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.en_traitement)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4,5,6,7],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Window": {
                        "Count": 500
                      }
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0,
                          1,
                          2,
                          3,
                          4,
                          5,
                          6,
                          7
                        ],
                        "Subtotal": 1
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "cases_data23042020",
                      "Name": "c"
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c"
                          }
                        },
                        "Property": "admin0Name"
                      },
                      "Name": "cases_data23042020.admin0Name"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c"
                          }
                        },
                        "Property": "admin1Name"
                      },
                      "Name": "cases_data23042020.admin1Name"
                    },
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "c"
                              }
                            },
                            "Property": "Contacts_suivis"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.Contacts_suivis)"
                    },
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "c"
                              }
                            },
                            "Property": "Tests_effectues"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.Tests_effectues)"
                    },
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "c"
                              }
                            },
                            "Property": "cas_confirm\u00e9s"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.cas_confirm\u00e9s)"
                    },
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "c"
                              }
                            },
                            "Property": "Gueris"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.Gueris)"
                    },
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "c"
                              }
                            },
                            "Property": "d\u00e9c\u00e8s"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.d\u00e9c\u00e8s)"
                    },
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "c"
                              }
                            },
                            "Property": "en_traitement"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.en_traitement)"
                    }
                  ],
                  "Version": 2
                }
              }
            }
          ]
        },
        "QueryId": ""
      }


country_data_2_req = {
    "ApplicationContext": {
        "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
        "Sources": [
            {
                "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"cases_data23042020\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"},\"Name\":\"cases_data23042020.admin0Name\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin1Name\"},\"Name\":\"cases_data23042020.admin1Name\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Contacts_suivis\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Contacts_suivis)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Tests_effectues\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Tests_effectues)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.cas_confirm\u00e9s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Gueris)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"d\u00e9c\u00e8s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.d\u00e9c\u00e8s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"en_traitement\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.en_traitement)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4,5,6,7],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "DataReduction": {
                            "DataVolume": 3,
                            "Primary": {
                                "Window": {
                                    "Count": 500
                                }
                            }
                        },
                        "Primary": {
                            "Groupings": [
                                {
                                    "Projections": [
                                        0,
                                        1,
                                        2,
                                        3,
                                        4,
                                        5,
                                        6,
                                        7
                                    ],
                                    "Subtotal": 1
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "cases_data23042020",
                                "Name": "c",
                                "Type": 0
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "c"
                                        }
                                    },
                                    "Property": "admin0Name"
                                },
                                "Name": "cases_data23042020.admin0Name"
                            },
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "c"
                                        }
                                    },
                                    "Property": "admin1Name"
                                },
                                "Name": "cases_data23042020.admin1Name"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c"
                                                }
                                            },
                                            "Property": "Contacts_suivis"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.Contacts_suivis)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c"
                                                }
                                            },
                                            "Property": "Tests_effectues"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.Tests_effectues)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c"
                                                }
                                            },
                                            "Property": "cas_confirm\u00e9s"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.cas_confirm\u00e9s)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c"
                                                }
                                            },
                                            "Property": "Gueris"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.Gueris)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c"
                                                }
                                            },
                                            "Property": "d\u00e9c\u00e8s"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.d\u00e9c\u00e8s)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c"
                                                }
                                            },
                                            "Property": "en_traitement"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.en_traitement)"
                            }
                        ],
                        "Version": 2
                    }
                }
            }
        ]
    },
    "QueryId": ""
}


if __name__ == '__main__':
    wapb = WestAfricaPowerBI()
    wapb.run_powerbi_grabber()
