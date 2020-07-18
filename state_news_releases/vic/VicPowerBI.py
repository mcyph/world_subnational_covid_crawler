import os
from covid_19_au_grab.state_news_releases.PowerBIBase import \
    PowerBIBase
from covid_19_au_grab.get_package_dir import get_data_dir


class VicPowerBI(PowerBIBase):
    PATH_PREFIX = get_data_dir() / 'vic' / 'powerbi'
    POWERBI_URL = (
        "https://app.powerbi.com/view?r=eyJrIjoiODBmMmE3NWQt"
        "ZWNlNC00OWRkLTk1NjYtMjM2YTY1MjI2NzdjIiwidCI6ImMwZTA"
        "2MDFmLTBmYWMtNDQ5Yy05Yzg4LWExMDRjNGViOWYyOCJ9"
    )
    def __init__(self):
        PowerBIBase.__init__(self,
                             self.PATH_PREFIX,
                             globals(),
                             self.POWERBI_URL)


def get_globals():
    return globals()


true = True
false = False

source_of_infection_2_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
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
                                "Top": {}
                            }
                        },
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
                                "Entity": "Linelist",
                                "Name": "l"
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "l"
                                            }
                                        },
                                        "Property": "Cases"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "acquired_n"
                                },
                                "Name": "Linelist.acquired_n"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
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

source_of_infection_3_req = {
    "ApplicationContext": {
        "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
        "Sources": [
            {
                "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"s\",\"Entity\":\"Source Table\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases (%)\"},\"Name\":\"Table.Confirmed Cases (%)\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Source_1\"},\"Name\":\"Sheet1.Source_1\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Source (new)\"},\"Name\":\"Sheet1.Source (new)\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases (%)\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,0],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                                        1,
                                        0
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
                                "Entity": "Table",
                                "Name": "t"
                            },
                            {
                                "Entity": "Source Table",
                                "Name": "s"
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "t"
                                            }
                                        },
                                        "Property": "Confirmed Cases (%)"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "t"
                                        }
                                    },
                                    "Property": "Confirmed Cases (%)"
                                },
                                "Name": "Table.Confirmed Cases (%)"
                            },
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "s"
                                        }
                                    },
                                    "Property": "Source_1"
                                },
                                "Name": "Sheet1.Source_1"
                            },
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "s"
                                        }
                                    },
                                    "Property": "Source (new)"
                                },
                                "Name": "Sheet1.Source (new)"
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

age_data_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimAgeGroup\"},{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"},\"Name\":\"dimAgeGroup.AgeGroup\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Sex\"},\"Name\":\"Linelist.Sex\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Measure\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"M_Age_MedianANDRange\"},\"Name\":\"Linelist.M_Age_MedianANDRange\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,2],\"ShowItemsWithNoData\":[0]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[1]}]},\"Projections\":[3],\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 4,
                    "Primary": {
                      "Window": {
                        "Count": 200
                      }
                    },
                    "Secondary": {
                      "Top": {
                        "Count": 60
                      }
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0,
                          2
                        ],
                        "ShowItemsWithNoData": [
                          0
                        ]
                      }
                    ]
                  },
                  "Projections": [
                    3
                  ],
                  "Secondary": {
                    "Groupings": [
                      {
                        "Projections": [
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
                      "Entity": "dimAgeGroup",
                      "Name": "d"
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "d"
                            }
                          },
                          "Property": "AgeGroup"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d"
                          }
                        },
                        "Property": "AgeGroup"
                      },
                      "Name": "dimAgeGroup.AgeGroup"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "Linelist.Sex"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Measure"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "M_Age_MedianANDRange"
                      },
                      "Name": "Linelist.M_Age_MedianANDRange"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "Not": {
                          "Expression": {
                            "Comparison": {
                              "ComparisonKind": 0,
                              "Left": {
                                "Column": {
                                  "Expression": {
                                    "SourceRef": {
                                      "Source": "d"
                                    }
                                  },
                                  "Property": "AgeGroup"
                                }
                              },
                              "Right": {
                                "Literal": {
                                  "Value": "null"
                                }
                              }
                            }
                          }
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

age_median_range_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"M_Age_MedianANDRange\"},\"Name\":\"Linelist.M_Age_MedianANDRange\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Linelist",
                                        "Name": "l"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Measure": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "l"
                                                }
                                            },
                                            "Property": "M_Age_MedianANDRange"
                                        },
                                        "Name": "Linelist.M_Age_MedianANDRange"
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

deceased_total_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"M_Deaths\"},\"Name\":\"Linelist.M_Deaths\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Deceased'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "M_Deaths"
                      },
                      "Name": "Linelist.M_Deaths"
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
                                    "Source": "l"
                                  }
                                },
                                "Property": "clin_status_n"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Deceased'"
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

tested_total_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"tested\"}},\"Function\":3},\"Name\":\"Min(Tested.tested)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Tested",
                      "Name": "t"
                    }
                  ],
                  "Select": [
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "t"
                              }
                            },
                            "Property": "tested"
                          }
                        },
                        "Function": 3
                      },
                      "Name": "Min(Tested.tested)"
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

male_female_balance_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Sex\"},\"Name\":\"Linelist.Sex\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
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
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 2,
                      "Expression": {
                        "Measure": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "l"
                            }
                          },
                          "Property": "Cases"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "Linelist.Sex"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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

regions_2_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d1\",\"Entity\":\"dimLGA\"},{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                      "Entity": "dimLGA",
                      "Name": "d1"
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d1"
                          }
                        },
                        "Property": "LGAName"
                      },
                      "Name": "dimLGA.LGAName"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "Not": {
                          "Expression": {
                            "Comparison": {
                              "ComparisonKind": 0,
                              "Left": {
                                "Column": {
                                  "Expression": {
                                    "SourceRef": {
                                      "Source": "d1"
                                    }
                                  },
                                  "Property": "LGAName"
                                }
                              },
                              "Right": {
                                "Literal": {
                                  "Value": "null"
                                }
                              }
                            }
                          }
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

regions_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d1\",\"Entity\":\"dimLGA\"},{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                      "Entity": "dimLGA",
                      "Name": "d1"
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d1"
                          }
                        },
                        "Property": "LGAName"
                      },
                      "Name": "dimLGA.LGAName"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "Not": {
                          "Expression": {
                            "Comparison": {
                              "ComparisonKind": 0,
                              "Left": {
                                "Column": {
                                  "Expression": {
                                    "SourceRef": {
                                      "Source": "d1"
                                    }
                                  },
                                  "Property": "LGAName"
                                }
                              },
                              "Right": {
                                "Literal": {
                                  "Value": "null"
                                }
                              }
                            }
                          }
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

regions_2_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimLGA\"},{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":1,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "Aggregates": [
                    {
                      "Aggregations": [
                        {
                          "Min": {}
                        },
                        {
                          "Max": {}
                        }
                      ],
                      "Select": 1
                    }
                  ],
                  "DataReduction": {
                    "DataVolume": 4,
                    "Primary": {
                      "Top": {}
                    }
                  },
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
                      "Entity": "dimLGA",
                      "Name": "d"
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 2,
                      "Expression": {
                        "Measure": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "l"
                            }
                          },
                          "Property": "Cases"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d"
                          }
                        },
                        "Property": "LGAName"
                      },
                      "Name": "dimLGA.LGAName"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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

#tested_total_req = {"version":"1.0.0","queries":[{"Query":{"Commands":[{"SemanticQueryDataShapeCommand":
#                                                                          {"Query":{"Version":2,"From":[{"Name":"t","Entity":"Tested"}],
#                                                                                    "Select":[{"Aggregation":{"Expression":{"Column":
#                                                                                                                              {"Expression":{"SourceRef":{"Source":"t"}},
#                                                                                                                               "Property":"tested"}},"Function":0},
#                                                                                               "Name":"Sum(Tested.tested)"}]},
#                                                                           "Binding":{"Primary":{"Groupings":[{"Projections":[0]}]},
#                                                                                      "DataReduction":{"DataVolume":3,"Primary":{"Top":{}}},"Version":1}}}]},
#                                                  "CacheKey":"{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"tested\"}},\"Function\":0},\"Name\":\"Sum(Tested.tested)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}","QueryId":"","ApplicationContext":{"DatasetId":"5b547437-24c9-4b22-92de-900b3b3f4785","Sources":[{"ReportId":"964ef513-8ff4-407c-8068-ade1e7f64ca5"}]}}],"cancelQueries":[],"modelId":1959902}

total_cases_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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

unknown_please_categorize_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"PHESSID\"}},\"Function\":5},\"Name\":\"Min(Linelist.PHESSID)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Localgovernmentarea\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Unknown'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Linelist",
                                        "Name": "l"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "PHESSID"
                                                }
                                            },
                                            "Function": 5
                                        },
                                        "Name": "Min(Linelist.PHESSID)"
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
                                                                    "Source": "l"
                                                                }
                                                            },
                                                            "Property": "Localgovernmentarea"
                                                        }
                                                    }
                                                ],
                                                "Values": [
                                                    [
                                                        {
                                                            "Literal": {
                                                                "Value": "'Unknown'"
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

overseas_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"PHESSID\"}},\"Function\":5},\"Name\":\"Min(Linelist.PHESSID)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Localgovernmentarea\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Overseas'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Linelist",
                                        "Name": "l"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "PHESSID"
                                                }
                                            },
                                            "Function": 5
                                        },
                                        "Name": "Min(Linelist.PHESSID)"
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
                                                                    "Source": "l"
                                                                }
                                                            },
                                                            "Property": "Localgovernmentarea"
                                                        }
                                                    }
                                                ],
                                                "Values": [
                                                    [
                                                        {
                                                            "Literal": {
                                                                "Value": "'Overseas'"
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

confirmed_cases_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"PHESSID\"}},\"Function\":5},\"Name\":\"Min(Linelist.PHESSID)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Linelist",
                                        "Name": "l"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "PHESSID"
                                                }
                                            },
                                            "Function": 5
                                        },
                                        "Name": "Min(Linelist.PHESSID)"
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

recovered_cases_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"PHESSID\"}},\"Function\":5},\"Name\":\"Min(Linelist.PHESSID)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Well, isolation complete'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Linelist",
                                        "Name": "l"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "PHESSID"
                                                }
                                            },
                                            "Function": 5
                                        },
                                        "Name": "Min(Linelist.PHESSID)"
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
                                                                    "Source": "l"
                                                                }
                                                            },
                                                            "Property": "clin_status_n"
                                                        }
                                                    }
                                                ],
                                                "Values": [
                                                    [
                                                        {
                                                            "Literal": {
                                                                "Value": "'Well, isolation complete'"
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

unknown_please_categorize_2_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"PHESSID\"}},\"Function\":5},\"Name\":\"CountNonNull(Linelist.PHESSID)\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Sex\"},\"Name\":\"Linelist.Sex\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"PHESSID\"}},\"Function\":5}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
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
                                        "Entity": "Linelist",
                                        "Name": "l"
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
                                                                "Source": "l"
                                                            }
                                                        },
                                                        "Property": "PHESSID"
                                                    }
                                                },
                                                "Function": 5
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
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "PHESSID"
                                                }
                                            },
                                            "Function": 5
                                        },
                                        "Name": "CountNonNull(Linelist.PHESSID)"
                                    },
                                    {
                                        "Column": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "l"
                                                }
                                            },
                                            "Property": "Sex"
                                        },
                                        "Name": "Linelist.Sex"
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

unknown_please_categorize_3_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"f\",\"Entity\":\"Filelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"f\"}},\"Property\":\"ModifiedLocal\"}},\"Function\":4},\"Name\":\"Min(Filelist.ModifiedLocal)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Filelist",
                                        "Name": "f"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "f"
                                                        }
                                                    },
                                                    "Property": "ModifiedLocal"
                                                }
                                            },
                                            "Function": 4
                                        },
                                        "Name": "Min(Filelist.ModifiedLocal)"
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

recovered_cases_2_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"PHESSID\"}},\"Function\":5},\"Name\":\"Min(Linelist.PHESSID)\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Well, isolation complete'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Linelist",
                                        "Name": "l"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "PHESSID"
                                                }
                                            },
                                            "Function": 5
                                        },
                                        "Name": "Min(Linelist.PHESSID)"
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
                                                                    "Source": "l"
                                                                }
                                                            },
                                                            "Property": "clin_status_n"
                                                        }
                                                    }
                                                ],
                                                "Values": [
                                                    [
                                                        {
                                                            "Literal": {
                                                                "Value": "'Well, isolation complete'"
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

median_age_range_age_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"M_Age_MedianANDRange\"},\"Name\":\"Linelist.M_Age_MedianANDRange\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Linelist",
                                        "Name": "l"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Measure": {
                                            "Expression": {
                                                "SourceRef": {
                                                    "Source": "l"
                                                }
                                            },
                                            "Property": "M_Age_MedianANDRange"
                                        },
                                        "Name": "Linelist.M_Age_MedianANDRange"
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

unknown_please_categorize_4_req = {
            "ApplicationContext": {
                "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
                "Sources": [
                    {
                        "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
                    }
                ]
            },
            "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"f\",\"Entity\":\"Filelist\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"f\"}},\"Property\":\"ModifiedLocal\"}},\"Function\":4},\"Name\":\"Min(Filelist.ModifiedLocal)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
            "Query": {
                "Commands": [
                    {
                        "SemanticQueryDataShapeCommand": {
                            "Binding": {
                                "DataReduction": {
                                    "DataVolume": 3,
                                    "Primary": {
                                        "Top": {}
                                    }
                                },
                                "Primary": {
                                    "Groupings": [
                                        {
                                            "Projections": [
                                                0
                                            ]
                                        }
                                    ]
                                },
                                "Version": 1
                            },
                            "Query": {
                                "From": [
                                    {
                                        "Entity": "Filelist",
                                        "Name": "f"
                                    }
                                ],
                                "Select": [
                                    {
                                        "Aggregation": {
                                            "Expression": {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "f"
                                                        }
                                                    },
                                                    "Property": "ModifiedLocal"
                                                }
                                            },
                                            "Function": 4
                                        },
                                        "Name": "Min(Filelist.ModifiedLocal)"
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

source_of_infection_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"acquired_n\"},\"Name\":\"Linelist.acquired_n\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
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
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 2,
                      "Expression": {
                        "Measure": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "l"
                            }
                          },
                          "Property": "Cases"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "acquired_n"
                      },
                      "Name": "Linelist.acquired_n"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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

running_total_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"s\",\"Entity\":\"Summarised\"},{\"Name\":\"d\",\"Entity\":\"dimDate\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"RunningTotal\"}},\"Function\":0},\"Name\":\"Sum(Summarised.RunningTotal)\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"},\"Name\":\"dimDate.Date\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,0],\"ShowItemsWithNoData\":[1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Sample\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 4,
                    "Primary": {
                      "Sample": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          1,
                          0
                        ],
                        "ShowItemsWithNoData": [
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
                      "Entity": "Summarised",
                      "Name": "s"
                    },
                    {
                      "Entity": "dimDate",
                      "Name": "d"
                    }
                  ],
                  "Select": [
                    {
                      "Aggregation": {
                        "Expression": {
                          "Column": {
                            "Expression": {
                              "SourceRef": {
                                "Source": "s"
                              }
                            },
                            "Property": "RunningTotal"
                          }
                        },
                        "Function": 0
                      },
                      "Name": "Sum(Summarised.RunningTotal)"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d"
                          }
                        },
                        "Property": "Date"
                      },
                      "Name": "dimDate.Date"
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

total_updated_date_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"M_LastUpdated\"},\"Name\":\"Tested.M_LastUpdated\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Tested",
                      "Name": "t"
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "M_LastUpdated"
                      },
                      "Name": "Tested.M_LastUpdated"
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

tested_well_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Well, isolation complete'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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
                                    "Source": "l"
                                  }
                                },
                                "Property": "clin_status_n"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Well, isolation complete'"
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

regions_active_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d1\",\"Entity\":\"dimLGA\"},{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}},{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                      "Entity": "dimLGA",
                      "Name": "d1"
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l"
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d1"
                          }
                        },
                        "Property": "LGAName"
                      },
                      "Name": "dimLGA.LGAName"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "Not": {
                          "Expression": {
                            "Comparison": {
                              "ComparisonKind": 0,
                              "Left": {
                                "Column": {
                                  "Expression": {
                                    "SourceRef": {
                                      "Source": "d1"
                                    }
                                  },
                                  "Property": "LGAName"
                                }
                              },
                              "Right": {
                                "Literal": {
                                  "Value": "null"
                                }
                              }
                            }
                          }
                        }
                      }
                    },
                    {
                      "Condition": {
                        "In": {
                          "Expressions": [
                            {
                              "Column": {
                                "Expression": {
                                  "SourceRef": {
                                    "Source": "l"
                                  }
                                },
                                "Property": "clin_status_n"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted to ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted, not known to be in ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Home isolation'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hospital in the home'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hotel detention'"
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


regions_active_2_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimLGA\"},{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":1,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1}}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "Aggregates": [
                            {
                                "Aggregations": [
                                    {
                                        "Min": {}
                                    },
                                    {
                                        "Max": {}
                                    }
                                ],
                                "Select": 1
                            }
                        ],
                        "DataReduction": {
                            "DataVolume": 4,
                            "Primary": {
                                "Top": {}
                            }
                        },
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
                                "Entity": "dimLGA",
                                "Name": "d"
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l"
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "l"
                                            }
                                        },
                                        "Property": "Cases"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
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
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "clin_status_n"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted to ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted, not known to be in ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Home isolation'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hospital in the home'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hotel detention'"
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

regions_3_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
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
                                "Entity": "dimLGA",
                                "Name": "d1"
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l"
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d1"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "Not": {
                                        "Expression": {
                                            "Comparison": {
                                                "ComparisonKind": 0,
                                                "Left": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "d1"
                                                            }
                                                        },
                                                        "Property": "LGAName"
                                                    }
                                                },
                                                "Right": {
                                                    "Literal": {
                                                        "Value": "null"
                                                    }
                                                }
                                            }
                                        }
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

regions_4_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d1\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
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
                                        1
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "dimLGA",
                                "Name": "d1",
                                "Type": 0
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l",
                                "Type": 0
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d1"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "Not": {
                                        "Expression": {
                                            "Comparison": {
                                                "ComparisonKind": 0,
                                                "Left": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "d1"
                                                            }
                                                        },
                                                        "Property": "LGAName"
                                                    }
                                                },
                                                "Right": {
                                                    "Literal": {
                                                        "Value": "null"
                                                    }
                                                }
                                            }
                                        }
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

age_data_2_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimAgeGroup\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"},\"Name\":\"dimAgeGroup.AgeGroup\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Sex\"},\"Name\":\"Linelist.Sex\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Measure\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"M_Age_MedianANDRange\"},\"Name\":\"Linelist.M_Age_MedianANDRange\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,2],\"ShowItemsWithNoData\":[0]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[1]}]},\"Projections\":[3],\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "DataReduction": {
                            "DataVolume": 4,
                            "Primary": {
                                "Window": {
                                    "Count": 200
                                }
                            },
                            "Secondary": {
                                "Top": {
                                    "Count": 60
                                }
                            }
                        },
                        "Primary": {
                            "Groupings": [
                                {
                                    "Projections": [
                                        0,
                                        2
                                    ],
                                    "ShowItemsWithNoData": [
                                        0
                                    ]
                                }
                            ]
                        },
                        "Projections": [
                            3
                        ],
                        "Secondary": {
                            "Groupings": [
                                {
                                    "Projections": [
                                        1
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "dimAgeGroup",
                                "Name": "d",
                                "Type": 0
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l",
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
                                                "Source": "d"
                                            }
                                        },
                                        "Property": "AgeGroup"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d"
                                        }
                                    },
                                    "Property": "AgeGroup"
                                },
                                "Name": "dimAgeGroup.AgeGroup"
                            },
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Sex"
                                },
                                "Name": "Linelist.Sex"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Measure"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "M_Age_MedianANDRange"
                                },
                                "Name": "Linelist.M_Age_MedianANDRange"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "Not": {
                                        "Expression": {
                                            "Comparison": {
                                                "ComparisonKind": 0,
                                                "Left": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "d"
                                                            }
                                                        },
                                                        "Property": "AgeGroup"
                                                    }
                                                },
                                                "Right": {
                                                    "Literal": {
                                                        "Value": "null"
                                                    }
                                                }
                                            }
                                        }
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

source_of_infection_4_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"acquired_n\"},\"Name\":\"Linelist.acquired_n\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "DataReduction": {
                            "DataVolume": 3,
                            "Primary": {
                                "Top": {}
                            }
                        },
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
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "Linelist",
                                "Name": "l",
                                "Type": 0
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "l"
                                            }
                                        },
                                        "Property": "Cases"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "acquired_n"
                                },
                                "Name": "Linelist.acquired_n"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
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

regions_active_3_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d1\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}},{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
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
                                        1
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "dimLGA",
                                "Name": "d1",
                                "Type": 0
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l",
                                "Type": 0
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d1"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "Not": {
                                        "Expression": {
                                            "Comparison": {
                                                "ComparisonKind": 0,
                                                "Left": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "d1"
                                                            }
                                                        },
                                                        "Property": "LGAName"
                                                    }
                                                },
                                                "Right": {
                                                    "Literal": {
                                                        "Value": "null"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "Condition": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "clin_status_n"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted to ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted, not known to be in ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Home isolation'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hospital in the home'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hotel detention'"
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

regions_active_6_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":1,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "Aggregates": [
                    {
                      "Aggregations": [
                        {
                          "Min": {}
                        },
                        {
                          "Max": {}
                        }
                      ],
                      "Select": 1
                    }
                  ],
                  "DataReduction": {
                    "DataVolume": 4,
                    "Primary": {
                      "Top": {}
                    }
                  },
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
                      "Entity": "dimLGA",
                      "Name": "d",
                      "Type": 0
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l",
                      "Type": 0
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 2,
                      "Expression": {
                        "Measure": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "l"
                            }
                          },
                          "Property": "Cases"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d"
                          }
                        },
                        "Property": "LGAName"
                      },
                      "Name": "dimLGA.LGAName"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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
                                    "Source": "l"
                                  }
                                },
                                "Property": "clin_status_n"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted to ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted, not known to be in ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Home isolation'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hospital in the home'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hotel detention'"
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


active_updated_date_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"M_LastUpdated\"},\"Name\":\"Tested.M_LastUpdated\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "ExecutionMetricsKind": 3,
                "Query": {
                  "From": [
                    {
                      "Entity": "Tested",
                      "Name": "t",
                      "Type": 0
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l",
                      "Type": 0
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "M_LastUpdated"
                      },
                      "Name": "Tested.M_LastUpdated"
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
                                    "Source": "l"
                                  }
                                },
                                "Property": "clin_status_n"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted to ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted, not known to be in ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Home isolation'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hospital in the home'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hotel detention'"
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

active_updated_date_2_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\"},{\"Name\":\"l\",\"Entity\":\"Linelist\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"M_LastUpdated\"},\"Name\":\"Tested.M_LastUpdated\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "DataReduction": {
                            "DataVolume": 3,
                            "Primary": {
                                "Top": {}
                            }
                        },
                        "Primary": {
                            "Groupings": [
                                {
                                    "Projections": [
                                        0
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "Query": {
                        "From": [
                            {
                                "Entity": "Tested",
                                "Name": "t"
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l"
                            }
                        ],
                        "Select": [
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "t"
                                        }
                                    },
                                    "Property": "M_LastUpdated"
                                },
                                "Name": "Tested.M_LastUpdated"
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
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "clin_status_n"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted to ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted, not known to be in ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Home isolation'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hospital in the home'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hotel detention'"
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

active_updated_date_3_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"M_LastUpdated\"},\"Name\":\"Tested.M_LastUpdated\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Tested",
                      "Name": "t",
                      "Type": 0
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l",
                      "Type": 0
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "M_LastUpdated"
                      },
                      "Name": "Tested.M_LastUpdated"
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
                                    "Source": "l"
                                  }
                                },
                                "Property": "clin_status_n"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted to ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted, not known to be in ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Home isolation'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hospital in the home'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hotel detention'"
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

total_updated_date_2_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"M_LastUpdated\"},\"Name\":\"Tested.M_LastUpdated\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Tested",
                      "Name": "t",
                      "Type": 0
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "M_LastUpdated"
                      },
                      "Name": "Tested.M_LastUpdated"
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

total_updated_date_3_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Tested\",\"Type\":0}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"M_LastUpdated\"},\"Name\":\"Tested.M_LastUpdated\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "ExecutionMetricsKind": 3,
                "Query": {
                  "From": [
                    {
                      "Entity": "Tested",
                      "Name": "t",
                      "Type": 0
                    }
                  ],
                  "Select": [
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "M_LastUpdated"
                      },
                      "Name": "Tested.M_LastUpdated"
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

regions_5_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":1,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "Aggregates": [
                            {
                                "Aggregations": [
                                    {
                                        "Min": {}
                                    },
                                    {
                                        "Max": {}
                                    }
                                ],
                                "Select": 1
                            }
                        ],
                        "DataReduction": {
                            "DataVolume": 4,
                            "Primary": {
                                "Top": {}
                            }
                        },
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
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "dimLGA",
                                "Name": "d",
                                "Type": 0
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l",
                                "Type": 0
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "l"
                                            }
                                        },
                                        "Property": "Cases"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
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

regions_active_4_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":1,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "Aggregates": [
                            {
                                "Aggregations": [
                                    {
                                        "Min": {}
                                    },
                                    {
                                        "Max": {}
                                    }
                                ],
                                "Select": 1
                            }
                        ],
                        "DataReduction": {
                            "DataVolume": 4,
                            "Primary": {
                                "Top": {}
                            }
                        },
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
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "dimLGA",
                                "Name": "d",
                                "Type": 0
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l",
                                "Type": 0
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "l"
                                            }
                                        },
                                        "Property": "Cases"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
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
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "clin_status_n"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted to ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted, not known to be in ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Home isolation'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hospital in the home'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hotel detention'"
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

regions_active_5_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":1,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1},\"ExecutionMetricsKind\":3}}]}",
    "Query": {
        "Commands": [
            {
                "SemanticQueryDataShapeCommand": {
                    "Binding": {
                        "Aggregates": [
                            {
                                "Aggregations": [
                                    {
                                        "Min": {}
                                    },
                                    {
                                        "Max": {}
                                    }
                                ],
                                "Select": 1
                            }
                        ],
                        "DataReduction": {
                            "DataVolume": 4,
                            "Primary": {
                                "Top": {}
                            }
                        },
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
                    "ExecutionMetricsKind": 3,
                    "Query": {
                        "From": [
                            {
                                "Entity": "dimLGA",
                                "Name": "d",
                                "Type": 0
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l",
                                "Type": 0
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 2,
                                "Expression": {
                                    "Measure": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "l"
                                            }
                                        },
                                        "Property": "Cases"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
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
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "clin_status_n"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted to ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted, not known to be in ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Home isolation'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hospital in the home'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hotel detention'"
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

regions_6_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":1,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "Aggregates": [
                    {
                      "Aggregations": [
                        {
                          "Min": {}
                        },
                        {
                          "Max": {}
                        }
                      ],
                      "Select": 1
                    }
                  ],
                  "DataReduction": {
                    "DataVolume": 4,
                    "Primary": {
                      "Top": {}
                    }
                  },
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
                      "Entity": "dimLGA",
                      "Name": "d",
                      "Type": 0
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l",
                      "Type": 0
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 2,
                      "Expression": {
                        "Measure": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "l"
                            }
                          },
                          "Property": "Cases"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d"
                          }
                        },
                        "Property": "LGAName"
                      },
                      "Name": "dimLGA.LGAName"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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

age_data_3_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"dimAgeGroup\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"},\"Name\":\"dimAgeGroup.AgeGroup\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Sex\"},\"Name\":\"Linelist.Sex\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Measure\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"M_Age_MedianANDRange\"},\"Name\":\"Linelist.M_Age_MedianANDRange\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"AgeGroup\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,2],\"ShowItemsWithNoData\":[0]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[1]}]},\"Projections\":[3],\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 4,
                    "Primary": {
                      "Window": {
                        "Count": 200
                      }
                    },
                    "Secondary": {
                      "Top": {
                        "Count": 60
                      }
                    }
                  },
                  "Primary": {
                    "Groupings": [
                      {
                        "Projections": [
                          0,
                          2
                        ],
                        "ShowItemsWithNoData": [
                          0
                        ]
                      }
                    ]
                  },
                  "Projections": [
                    3
                  ],
                  "Secondary": {
                    "Groupings": [
                      {
                        "Projections": [
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
                      "Entity": "dimAgeGroup",
                      "Name": "d",
                      "Type": 0
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l",
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
                              "Source": "d"
                            }
                          },
                          "Property": "AgeGroup"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d"
                          }
                        },
                        "Property": "AgeGroup"
                      },
                      "Name": "dimAgeGroup.AgeGroup"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "Linelist.Sex"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Measure"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "M_Age_MedianANDRange"
                      },
                      "Name": "Linelist.M_Age_MedianANDRange"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "Not": {
                          "Expression": {
                            "Comparison": {
                              "ComparisonKind": 0,
                              "Left": {
                                "Column": {
                                  "Expression": {
                                    "SourceRef": {
                                      "Source": "d"
                                    }
                                  },
                                  "Property": "AgeGroup"
                                }
                              },
                              "Right": {
                                "Literal": {
                                  "Value": "null"
                                }
                              }
                            }
                          }
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

source_of_infection_5_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"acquired_n\"},\"Name\":\"Linelist.acquired_n\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
        "Query": {
          "Commands": [
            {
              "SemanticQueryDataShapeCommand": {
                "Binding": {
                  "DataReduction": {
                    "DataVolume": 3,
                    "Primary": {
                      "Top": {}
                    }
                  },
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
                      "Entity": "Linelist",
                      "Name": "l",
                      "Type": 0
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 2,
                      "Expression": {
                        "Measure": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "l"
                            }
                          },
                          "Property": "Cases"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "acquired_n"
                      },
                      "Name": "Linelist.acquired_n"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
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

regions_active_7_req = {
    "ApplicationContext": {
        "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
        "Sources": [
            {
                "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d1\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}},{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                                "Entity": "dimLGA",
                                "Name": "d1",
                                "Type": 0
                            },
                            {
                                "Entity": "Linelist",
                                "Name": "l",
                                "Type": 0
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "d1"
                                        }
                                    },
                                    "Property": "LGAName"
                                },
                                "Name": "dimLGA.LGAName"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "l"
                                        }
                                    },
                                    "Property": "Cases"
                                },
                                "Name": "Linelist.Cases"
                            }
                        ],
                        "Version": 2,
                        "Where": [
                            {
                                "Condition": {
                                    "Not": {
                                        "Expression": {
                                            "Comparison": {
                                                "ComparisonKind": 0,
                                                "Left": {
                                                    "Column": {
                                                        "Expression": {
                                                            "SourceRef": {
                                                                "Source": "d1"
                                                            }
                                                        },
                                                        "Property": "LGAName"
                                                    }
                                                },
                                                "Right": {
                                                    "Literal": {
                                                        "Value": "null"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "Condition": {
                                    "In": {
                                        "Expressions": [
                                            {
                                                "Column": {
                                                    "Expression": {
                                                        "SourceRef": {
                                                            "Source": "l"
                                                        }
                                                    },
                                                    "Property": "clin_status_n"
                                                }
                                            }
                                        ],
                                        "Values": [
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted to ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Admitted, not known to be in ICU'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Home isolation'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hospital in the home'"
                                                    }
                                                }
                                            ],
                                            [
                                                {
                                                    "Literal": {
                                                        "Value": "'Hotel detention'"
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

regions_active_8_req = {
        "ApplicationContext": {
          "DatasetId": "5b547437-24c9-4b22-92de-900b3b3f4785",
          "Sources": [
            {
              "ReportId": "964ef513-8ff4-407c-8068-ade1e7f64ca5"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d1\",\"Entity\":\"dimLGA\",\"Type\":0},{\"Name\":\"l\",\"Entity\":\"Linelist\",\"Type\":0}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"},\"Name\":\"dimLGA.LGAName\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"Cases\"},\"Name\":\"Linelist.Cases\"}],\"Where\":[{\"Condition\":{\"Not\":{\"Expression\":{\"Comparison\":{\"ComparisonKind\":0,\"Left\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d1\"}},\"Property\":\"LGAName\"}},\"Right\":{\"Literal\":{\"Value\":\"null\"}}}}}}},{\"Condition\":{\"In\":{\"Expressions\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"l\"}},\"Property\":\"clin_status_n\"}}],\"Values\":[[{\"Literal\":{\"Value\":\"'Admitted to ICU'\"}}],[{\"Literal\":{\"Value\":\"'Admitted, not known to be in ICU'\"}}],[{\"Literal\":{\"Value\":\"'Home isolation'\"}}],[{\"Literal\":{\"Value\":\"'Hotel detention'\"}}],[{\"Literal\":{\"Value\":\"'Hospital in the home'\"}}],[{\"Literal\":{\"Value\":\"'Under investigation'\"}}]]}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                      "Entity": "dimLGA",
                      "Name": "d1",
                      "Type": 0
                    },
                    {
                      "Entity": "Linelist",
                      "Name": "l",
                      "Type": 0
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "d1"
                          }
                        },
                        "Property": "LGAName"
                      },
                      "Name": "dimLGA.LGAName"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "l"
                          }
                        },
                        "Property": "Cases"
                      },
                      "Name": "Linelist.Cases"
                    }
                  ],
                  "Version": 2,
                  "Where": [
                    {
                      "Condition": {
                        "Not": {
                          "Expression": {
                            "Comparison": {
                              "ComparisonKind": 0,
                              "Left": {
                                "Column": {
                                  "Expression": {
                                    "SourceRef": {
                                      "Source": "d1"
                                    }
                                  },
                                  "Property": "LGAName"
                                }
                              },
                              "Right": {
                                "Literal": {
                                  "Value": "null"
                                }
                              }
                            }
                          }
                        }
                      }
                    },
                    {
                      "Condition": {
                        "In": {
                          "Expressions": [
                            {
                              "Column": {
                                "Expression": {
                                  "SourceRef": {
                                    "Source": "l"
                                  }
                                },
                                "Property": "clin_status_n"
                              }
                            }
                          ],
                          "Values": [
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted to ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Admitted, not known to be in ICU'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Home isolation'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hotel detention'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Hospital in the home'"
                                }
                              }
                            ],
                            [
                              {
                                "Literal": {
                                  "Value": "'Under investigation'"
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
    vpb = VicPowerBI()
    vpb.run_powerbi_grabber()

