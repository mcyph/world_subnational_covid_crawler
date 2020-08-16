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

country_data_3_req = {
    "ApplicationContext": {
        "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
        "Sources": [
            {
                "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"cases_data23042020\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"},\"Name\":\"cases_data23042020.admin0Name\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin1Name\"},\"Name\":\"cases_data23042020.admin1Name\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.cas_confirm\u00e9s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"d\u00e9c\u00e8s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.d\u00e9c\u00e8s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"en_traitement\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.en_traitement)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Gueris)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Femmes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Femmes)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Hommes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Hommes)\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4,5,6,7],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
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
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
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
                                    }
                                }
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
                                            "Property": "Femmes"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.Femmes)"
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
                                            "Property": "Hommes"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.Hommes)"
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

IGNORE_country_data_4_req = {
    "ApplicationContext": {
        "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
        "Sources": [
            {
                "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c1\",\"Entity\":\"cases_data23042020\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"admin0Name\"},\"Name\":\"cases_data_23042020.admin0Name\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Gueris\"}},\"Function\":0},\"Name\":\"Sum(cases_data_23042020.Gueris)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"d\u00e9c\u00e8s\"}},\"Function\":0},\"Name\":\"Sum(cases_data_23042020.d\u00e9c\u00e8s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.cas_confirm\u00e9s)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Week\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Week 22'\"}}]]}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":1000}}},\"Version\":1}}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "DataReduction": {
                            "DataVolume": 4,
                            "Primary": {
                                "Window": {
                                    "Count": 1000
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
                                        3
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "Query": {
                        "From": [
                            {
                                "Entity": "cases_data23042020",
                                "Name": "c1"
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "c1"
                                                    }
                                                },
                                                "Property": "cas_confirm\u00e9s"
                                            }
                                        },
                                        "Function": 0
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "c1"
                                        }
                                    },
                                    "Property": "admin0Name"
                                },
                                "Name": "cases_data_23042020.admin0Name"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "Gueris"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data_23042020.Gueris)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "d\u00e9c\u00e8s"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data_23042020.d\u00e9c\u00e8s)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "cas_confirm\u00e9s"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.cas_confirm\u00e9s)"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "c1"
                                                        }
                                                    },
                                                    "Property": "Week"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Week 22'"
                                                    }
                                                }
                                            ]
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        ]
    },
    "QueryId": ""
}

IGNORE_country_data_5_req = {
    "ApplicationContext": {
        "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
        "Sources": [
            {
                "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
        ]
    },
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "DataReduction": {
                            "DataVolume": 3,
                            "Primary": {
                                "Sample": {
                                    "Count": 30000
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
                                        4
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "Query": {
                        "From": [
                            {
                                "Entity": "cases_data23042020",
                                "Name": "c1",
                                "Type": 0
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 1,
                                "Expression": {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "c1"
                                                    }
                                                },
                                                "Property": "admin0Name"
                                            }
                                        },
                                        "Function": 3
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "c1"
                                        }
                                    },
                                    "Property": "admin1Pcod"
                                },
                                "Name": "cases_data_23042020.admin1Pcod"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "L\u00e9gende"
                                        }
                                    },
                                    "Function": 3
                                },
                                "Name": "Min(cases_data23042020.L\u00e9gende)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "admin0Name"
                                        }
                                    },
                                    "Function": 3
                                },
                                "Name": "Min(cases_data23042020.admin0Name)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "admin1Name"
                                        }
                                    },
                                    "Function": 3
                                },
                                "Name": "Min(cases_data23042020.admin1Name)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "cas_confirm\u00e9s"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.cas_confirm\u00e9s)"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "c1"
                                                        }
                                                    },
                                                    "Property": "Week"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Week 28'"
                                                    }
                                                }
                                            ]
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        ]
    },
    "QueryId": ""
}

country_data_6_req = {
    "ApplicationContext": {
        "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
        "Sources": [
            {
                "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"cases_data23042020\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"},\"Name\":\"cases_data23042020.admin0Name\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin1Name\"},\"Name\":\"cases_data23042020.admin1Name\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.cas_confirm\u00e9s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"d\u00e9c\u00e8s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.d\u00e9c\u00e8s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"en_traitement\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.en_traitement)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Gueris)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Femmes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Femmes)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Hommes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Hommes)\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4,5,6,7],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                                "Name": "c",
                                "Type": 0
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
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
                                    }
                                }
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
                                            "Property": "Femmes"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.Femmes)"
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
                                            "Property": "Hommes"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data23042020.Hommes)"
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

country_data_7_req = {
    "ApplicationContext": {
        "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
        "Sources": [
            {
                "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c1\",\"Entity\":\"cases_data23042020\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Femmes\"}},\"Function\":0},\"Name\":\"Sum(cases_data_23042020.Femmes)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Hommes\"}},\"Function\":0},\"Name\":\"Sum(cases_data_23042020.Hommes)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Week\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Week 22'\"}}]]}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Femmes\"}},\"Function\":0}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"Version\":1}}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "Primary": {
                            "Groupings": [
                                {
                                    "Projections": [
                                        0,
                                        1
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "Query": {
                        "From": [
                            {
                                "Entity": "cases_data23042020",
                                "Name": "c1"
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Aggregation": {
                                        "Expression": {
                                            "Column": {
                                                "Expression": {
                                                    "SourceRef": {
                                                        "Source": "c1"
                                                    }
                                                },
                                                "Property": "Femmes"
                                            }
                                        },
                                        "Function": 0
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "Femmes"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data_23042020.Femmes)"
                            },
                            {
                                "Aggregation": {
                                    "Expression": {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "c1"
                                                }
                                            },
                                            "Property": "Hommes"
                                        }
                                    },
                                    "Function": 0
                                },
                                "Name": "Sum(cases_data_23042020.Hommes)"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "c1"
                                                        }
                                                    },
                                                    "Property": "Week"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Week 22'"
                                                    }
                                                }
                                            ]
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        ]
    },
    "QueryId": ""
}


country_data_8_req = {
        "ApplicationContext": {
          "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
          "Sources": [
            {
              "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"cases_data23042020\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"},\"Name\":\"cases_data23042020.admin0Name\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin1Name\"},\"Name\":\"cases_data23042020.admin1Name\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.cas_confirm\u00e9s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"d\u00e9c\u00e8s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.d\u00e9c\u00e8s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"en_traitement\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.en_traitement)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Gueris)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Femmes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Femmes)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Hommes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Hommes)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Week\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Week 31'\"}}]]}}}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4,5,6,7],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                      "Name": "c",
                      "Type": 0
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "c"
                            }
                          },
                          "Property": "admin0Name"
                        }
                      }
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
                            "Property": "Femmes"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.Femmes)"
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
                            "Property": "Hommes"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.Hommes)"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "In": {
                          "Expressions": [
                            {
                              "Column": {
                                "Expression": {
                                  "SourceRef": {
                                    "Source": "c"
                                  }
                                },
                                "Property": "Week"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Week 31'"
                                }
                              }
                            ]
                          ]
                        }
                      }
                    }
                  ]
                }
              }
            }
          ]
        },
        "QueryId": ""
      }

country_data_9_req = {
        "ApplicationContext": {
          "DatasetId": "bbedabd3-11a6-4f6c-86a9-4244f1092233",
          "Sources": [
            {
              "ReportId": "7c067b82-3dc8-42e6-b085-27a3fd78c990"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c\",\"Entity\":\"cases_data23042020\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"},\"Name\":\"cases_data23042020.admin0Name\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin1Name\"},\"Name\":\"cases_data23042020.admin1Name\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"cas_confirm\u00e9s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.cas_confirm\u00e9s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"d\u00e9c\u00e8s\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.d\u00e9c\u00e8s)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"en_traitement\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.en_traitement)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Gueris\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Gueris)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Femmes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Femmes)\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Hommes\"}},\"Function\":0},\"Name\":\"Sum(cases_data23042020.Hommes)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Week\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Week 32'\"}}]]}}}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"admin0Name\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1,2,3,4,5,6,7],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                      "Name": "c",
                      "Type": 0
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "c"
                            }
                          },
                          "Property": "admin0Name"
                        }
                      }
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
                            "Property": "Femmes"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.Femmes)"
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
                            "Property": "Hommes"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(cases_data23042020.Hommes)"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "In": {
                          "Expressions": [
                            {
                              "Column": {
                                "Expression": {
                                  "SourceRef": {
                                    "Source": "c"
                                  }
                                },
                                "Property": "Week"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Week 32'"
                                }
                              }
                            ]
                          ]
                        }
                      }
                    }
                  ]
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
