import os
from covid_19_au_grab.powerbi_grabber.PowerBIBase import \
    PowerBIBase


class VicPowerBI(PowerBIBase):
    def __init__(self):
        path_prefix = os.path.expanduser(
            f'~/dev/covid_19_data/vic/powerbi'
        )
        powerbi_url = (
            "https://app.powerbi.com/view?r=eyJrIjoiODBmMmE3NWQt"
            "ZWNlNC00OWRkLTk1NjYtMjM2YTY1MjI2NzdjIiwidCI6ImMwZTA"
            "2MDFmLTBmYWMtNDQ5Yy05Yzg4LWExMDRjNGViOWYyOCJ9"
        )
        PowerBIBase.__init__(self,
                             path_prefix,
                             globals(),
                             powerbi_url)


true = True
false = False

age_data_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
    ],
    "version": "1.0.0"
}

age_median_range_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
        {
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
    ],
    "version": "1.0.0"
}

tested_and_deceased_total_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
      },
      {
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
    ],
    "version": "1.0.0"
}

male_female_balance_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
    ],
    "version": "1.0.0"
}

regions_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
    ],
    "version": "1.0.0"
}

regions_2_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
    ],
    "version": "1.0.0"
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
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
    ],
    "version": "1.0.0"
}

unknown_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
        {
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
    ],
    "version": "1.0.0"
}

overseas_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
        {
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
    ],
    "version": "1.0.0"
}

confirmed_cases_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
        {
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
    ],
    "version": "1.0.0"
}

recovered_cases_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
        {
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
        },
        {
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
    ],
    "version": "1.0.0"
}

recovered_cases_2_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
        {
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
        },
        {
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
    ],
    "version": "1.0.0"
}

median_age_range_age_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
        {
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
        },
        {
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
    ],
    "version": "1.0.0"
}

source_of_infection_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
    ],
    "version": "1.0.0"
}

running_total_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
    ],
    "version": "1.0.0"
}

tested_well_req = {
    "cancelQueries": [],
    "modelId": 1959902,
    "queries": [
      {
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
      },
      {
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
    ],
    "version": "1.0.0"
}


if __name__ == '__main__':
    vpb = VicPowerBI()
    vpb.run_powerbi_grabber()

