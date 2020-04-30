import os
from covid_19_au_grab.state_news_releases.PowerBIBase import \
    PowerBIBase


class ACTPowerBI(PowerBIBase):
    PATH_PREFIX = os.path.expanduser(
        f'~/dev/covid_19_data/act/powerbi'
    )
    POWERBI_URL = (
        'https://app.powerbi.com/view?r=eyJrIjoiM2M4MGIxYTU'
        'tZjA1Yy00YTA4LTkwNDMtMDM4ZTdkMGZhN2ZiIiwidCI6ImI0N'
        'mMxOTA4LTAzMzQtNDIzNi1iOTc4LTU4NWVlODhlNDE5OSJ9'
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

regions_inexact_2_req = {
    "ApplicationContext": {
        "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
        "Sources": [
            {
                "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"s\",\"Entity\":\"Shape Map(SA3)\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"SA3\"},\"Name\":\"Shape Map(SA3).SA3 Name\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1],\"ShowItemsWithNoData\":[0,1],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                                    ],
                                    "ShowItemsWithNoData": [
                                        0,
                                        1
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
                                "Entity": "Shape Map(SA3)",
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
                                        "Property": "Count of Confirmed Cases"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "s"
                                        }
                                    },
                                    "Property": "SA3"
                                },
                                "Name": "Shape Map(SA3).SA3 Name"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "t"
                                        }
                                    },
                                    "Property": "Count of Confirmed Cases"
                                },
                                "Name": "Table.Count of Confirmed Cases"
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

age_groups_4_req = {
    "ApplicationContext": {
        "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
        "Sources": [
            {
                "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
        ]
    },
    "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"a1\",\"Entity\":\"Age Buckets (2)\"},{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"c\",\"Entity\":\"COVID%20Case%20Data%20(02042020)\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"},\"Name\":\"Age Buckets (2).Age Group\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Sex\"},\"Name\":\"COVID%20Case%20Data%20(02042020).Sex\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                                        1
                                    ]
                                }
                            ]
                        },
                        "Secondary": {
                            "Groupings": [
                                {
                                    "Projections": [
                                        2
                                    ]
                                }
                            ]
                        },
                        "Version": 1
                    },
                    "Query": {
                        "From": [
                            {
                                "Entity": "Age Buckets (2)",
                                "Name": "a1"
                            },
                            {
                                "Entity": "Table",
                                "Name": "t"
                            },
                            {
                                "Entity": "COVID%20Case%20Data%20(02042020)",
                                "Name": "c"
                            }
                        ],
                        "OrderBy": [
                            {
                                "Direction": 1,
                                "Expression": {
                                    "Column": {
                                        "Expression": {
                                            "SourceRef": {
                                                "Source": "a1"
                                            }
                                        },
                                        "Property": "Age group (years)"
                                    }
                                }
                            }
                        ],
                        "Select": [
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "a1"
                                        }
                                    },
                                    "Property": "Age group (years)"
                                },
                                "Name": "Age Buckets (2).Age Group"
                            },
                            {
                                "Measure": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "t"
                                        }
                                    },
                                    "Property": "Count of Confirmed Cases"
                                },
                                "Name": "Table.Count of Confirmed Cases"
                            },
                            {
                                "Column": {
                                    "Expression": {
                                        "SourceRef": {
                                            "Source": "c"
                                        }
                                    },
                                    "Property": "Sex"
                                },
                                "Name": "COVID%20Case%20Data%20(02042020).Sex"
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

age_groups_5_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"a1\",\"Entity\":\"Age Buckets\"},{\"Name\":\"t\",\"Entity\":\"Key Measures\"},{\"Name\":\"c\",\"Entity\":\"COVID%20Case%20Data%20(02042020)\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"},\"Name\":\"Age Buckets (2).Age Group\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Sex\"},\"Name\":\"COVID%20Case%20Data%20(02042020).Sex\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                          1
                        ]
                      }
                    ]
                  },
                  "Secondary": {
                    "Groupings": [
                      {
                        "Projections": [
                          2
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Age Buckets",
                      "Name": "a1"
                    },
                    {
                      "Entity": "Key Measures",
                      "Name": "t"
                    },
                    {
                      "Entity": "COVID%20Case%20Data%20(02042020)",
                      "Name": "c"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "a1"
                            }
                          },
                          "Property": "Age group (years)"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "a1"
                          }
                        },
                        "Property": "Age group (years)"
                      },
                      "Name": "Age Buckets (2).Age Group"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "Count of Confirmed Cases"
                      },
                      "Name": "Table.Count of Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "COVID%20Case%20Data%20(02042020).Sex"
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

age_groups_3_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c1\",\"Entity\":\"COVID Case Data 02042020\"},{\"Name\":\"a1\",\"Entity\":\"Age Buckets (2)\"},{\"Name\":\"t\",\"Entity\":\"Table\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Sex\"},\"Name\":\"COVID Case Data (02042020).Gender\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"},\"Name\":\"Age Buckets (2).Age Group\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,2]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                          1,
                          2
                        ]
                      }
                    ]
                  },
                  "Secondary": {
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
                      "Entity": "COVID Case Data 02042020",
                      "Name": "c1"
                    },
                    {
                      "Entity": "Age Buckets (2)",
                      "Name": "a1"
                    },
                    {
                      "Entity": "Table",
                      "Name": "t"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "a1"
                            }
                          },
                          "Property": "Age group (years)"
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
                        "Property": "Sex"
                      },
                      "Name": "COVID Case Data (02042020).Gender"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "a1"
                          }
                        },
                        "Property": "Age group (years)"
                      },
                      "Name": "Age Buckets (2).Age Group"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "Count of Confirmed Cases"
                      },
                      "Name": "Table.Count of Confirmed Cases"
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
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"d\",\"Entity\":\"Date\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Notifications\"},\"Name\":\"Table.Notifications\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"},\"Name\":\"Date.Date\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,0],\"ShowItemsWithNoData\":[1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":1000}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
                      "Name": "t"
                    },
                    {
                      "Entity": "Date",
                      "Name": "d"
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
                          "Property": "Date"
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
                        "Property": "Notifications"
                      },
                      "Name": "Table.Notifications"
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
                      "Name": "Date.Date"
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

age_groups_2_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c1\",\"Entity\":\"COVID Case Data 02042020\"},{\"Name\":\"a1\",\"Entity\":\"Age Buckets (2)\"},{\"Name\":\"t\",\"Entity\":\"Table\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Sex\"},\"Name\":\"COVID Case Data (02042020).Gender\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"},\"Name\":\"Age Buckets (2).Age Group\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,2]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                          1,
                          2
                        ]
                      }
                    ]
                  },
                  "Secondary": {
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
                      "Entity": "COVID Case Data 02042020",
                      "Name": "c1"
                    },
                    {
                      "Entity": "Age Buckets (2)",
                      "Name": "a1"
                    },
                    {
                      "Entity": "Table",
                      "Name": "t"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "a1"
                            }
                          },
                          "Property": "Age group (years)"
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
                        "Property": "Sex"
                      },
                      "Name": "COVID Case Data (02042020).Gender"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "a1"
                          }
                        },
                        "Property": "Age group (years)"
                      },
                      "Name": "Age Buckets (2).Age Group"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "Count of Confirmed Cases"
                      },
                      "Name": "Table.Count of Confirmed Cases"
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


recovered_2_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Recovered Cases\"},\"Name\":\"Table.Cases Cleared\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
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
                        "Property": "Recovered Cases"
                      },
                      "Name": "Table.Cases Cleared"
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

gender_balance_4_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Key Measures\"},{\"Name\":\"c\",\"Entity\":\"COVID%20Case%20Data%20(02042020)\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"},\"Name\":\"Table.Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Sex\"},\"Name\":\"COVID%20Case%20Data%20(02042020).Sex\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Key Measures",
                      "Name": "t"
                    },
                    {
                      "Entity": "COVID%20Case%20Data%20(02042020)",
                      "Name": "c"
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
                          "Property": "Confirmed Cases"
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
                        "Property": "Confirmed Cases"
                      },
                      "Name": "Table.Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "COVID%20Case%20Data%20(02042020).Sex"
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

gender_balance_2_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"c1\",\"Entity\":\"COVID Case Data 02042020\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"},\"Name\":\"Table.Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Sex\"},\"Name\":\"COVID Case Data (02042020).Gender\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
                      "Name": "t"
                    },
                    {
                      "Entity": "COVID Case Data 02042020",
                      "Name": "c1"
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
                          "Property": "Confirmed Cases"
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
                        "Property": "Confirmed Cases"
                      },
                      "Name": "Table.Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c1"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "COVID Case Data (02042020).Gender"
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

recovered_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Recovered Cases\"},\"Name\":\"Table.Cases Cleared\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
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
                        "Property": "Recovered Cases"
                      },
                      "Name": "Table.Cases Cleared"
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

deaths_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Deaths\"},\"Name\":\"Table.Deaths\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
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
                        "Property": "Deaths"
                      },
                      "Name": "Table.Deaths"
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

gender_balance_3_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"c\",\"Entity\":\"COVID%20Case%20Data%20(02042020)\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"},\"Name\":\"Table.Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Sex\"},\"Name\":\"COVID%20Case%20Data%20(02042020).Sex\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
                      "Name": "t"
                    },
                    {
                      "Entity": "COVID%20Case%20Data%20(02042020)",
                      "Name": "c"
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
                          "Property": "Confirmed Cases"
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
                        "Property": "Confirmed Cases"
                      },
                      "Name": "Table.Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "COVID%20Case%20Data%20(02042020).Sex"
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

unknown_please_categorize_me_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"d\",\"Entity\":\"Date Last Refreshed\"}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date Last Refreshed\"}},\"Function\":3},\"Name\":\"Min(Date Last Refreshed.Date Last Refreshed)\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Date Last Refreshed",
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
                                "Source": "d"
                              }
                            },
                            "Property": "Date Last Refreshed"
                          }
                        },
                        "Function": 3
                      },
                      "Name": "Min(Date Last Refreshed.Date Last Refreshed)"
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

gender_balance_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"c1\",\"Entity\":\"COVID Case Data 02042020\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"},\"Name\":\"Table.Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Sex\"},\"Name\":\"COVID Case Data (02042020).Gender\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
                      "Name": "t"
                    },
                    {
                      "Entity": "COVID Case Data 02042020",
                      "Name": "c1"
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
                          "Property": "Confirmed Cases"
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
                        "Property": "Confirmed Cases"
                      },
                      "Name": "Table.Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c1"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "COVID Case Data (02042020).Gender"
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


confirmed_cases_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"},\"Name\":\"Table.Total Notifications\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
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
                        "Property": "Confirmed Cases"
                      },
                      "Name": "Table.Total Notifications"
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

notifications_time_series_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"d\",\"Entity\":\"Date\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Notifications\"},\"Name\":\"Table.Notifications\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"},\"Name\":\"Date.Date\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,0],\"ShowItemsWithNoData\":[1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":1000}}},\"Version\":1}}}]}",
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
                      "Entity": "Table",
                      "Name": "t"
                    },
                    {
                      "Entity": "Date",
                      "Name": "d"
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
                          "Property": "Date"
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
                        "Property": "Notifications"
                      },
                      "Name": "Table.Notifications"
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
                      "Name": "Date.Date"
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

age_groups_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"c1\",\"Entity\":\"COVID Case Data 02042020\"},{\"Name\":\"a1\",\"Entity\":\"Age Buckets (2)\"},{\"Name\":\"t\",\"Entity\":\"Table\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c1\"}},\"Property\":\"Sex\"},\"Name\":\"COVID Case Data (02042020).Gender\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"},\"Name\":\"Age Buckets (2).Age Group\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,2]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                          1,
                          2
                        ]
                      }
                    ]
                  },
                  "Secondary": {
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
                      "Entity": "COVID Case Data 02042020",
                      "Name": "c1"
                    },
                    {
                      "Entity": "Age Buckets (2)",
                      "Name": "a1"
                    },
                    {
                      "Entity": "Table",
                      "Name": "t"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "a1"
                            }
                          },
                          "Property": "Age group (years)"
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
                        "Property": "Sex"
                      },
                      "Name": "COVID Case Data (02042020).Gender"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "a1"
                          }
                        },
                        "Property": "Age group (years)"
                      },
                      "Name": "Age Buckets (2).Age Group"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "Count of Confirmed Cases"
                      },
                      "Name": "Table.Count of Confirmed Cases"
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

regions_exact_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"s\",\"Entity\":\"Shape Map(SA3)\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"},\"Name\":\"Table.Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"SA3\"},\"Name\":\"Shape Map(SA3).SA3\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":0,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1}}}]}",
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
                      "Select": 0
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
                      "Entity": "Table",
                      "Name": "t"
                    },
                    {
                      "Entity": "Shape Map(SA3)",
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
                          "Property": "Confirmed Cases"
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
                        "Property": "Confirmed Cases"
                      },
                      "Name": "Table.Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "s"
                          }
                        },
                        "Property": "SA3"
                      },
                      "Name": "Shape Map(SA3).SA3"
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


regions_inexact_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"s\",\"Entity\":\"Shape Map(SA3)\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"SA3\"},\"Name\":\"Shape Map(SA3).SA3 Name\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"SA3\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1],\"ShowItemsWithNoData\":[0,1],\"Subtotal\":1}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Window\":{\"Count\":500}}},\"Version\":1}}}]}",
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
                        ],
                        "ShowItemsWithNoData": [
                          0,
                          1
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
                      "Entity": "Shape Map(SA3)",
                      "Name": "s"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "s"
                            }
                          },
                          "Property": "SA3"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "s"
                          }
                        },
                        "Property": "SA3"
                      },
                      "Name": "Shape Map(SA3).SA3 Name"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "Count of Confirmed Cases"
                      },
                      "Name": "Table.Count of Confirmed Cases"
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


infection_source_time_series_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"d\",\"Entity\":\"Date\"},{\"Name\":\"s\",\"Entity\":\"Source Table\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Notifications\"},\"Name\":\"Table.Epi Curve\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"},\"Name\":\"Date.Date\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Source_1\"},\"Name\":\"Sheet1.Source_1\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,0],\"ShowItemsWithNoData\":[1]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                          1,
                          0
                        ],
                        "ShowItemsWithNoData": [
                          1
                        ]
                      }
                    ]
                  },
                  "Secondary": {
                    "Groupings": [
                      {
                        "Projections": [
                          2
                        ]
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
                      "Entity": "Date",
                      "Name": "d"
                    },
                    {
                      "Entity": "Source Table",
                      "Name": "s"
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
                          "Property": "Date"
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
                        "Property": "Notifications"
                      },
                      "Name": "Table.Epi Curve"
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
                      "Name": "Date.Date"
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

infection_source_percentages_req = {
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

infection_source_time_series_2_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Key Measures\"},{\"Name\":\"d\",\"Entity\":\"Date\"},{\"Name\":\"s\",\"Entity\":\"Source Table\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Notifications\"},\"Name\":\"Table.Epi Curve\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"},\"Name\":\"Date.Date\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Source_1\"},\"Name\":\"Sheet1.Source_1\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"d\"}},\"Property\":\"Date\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[1,0],\"ShowItemsWithNoData\":[1]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                          1,
                          0
                        ],
                        "ShowItemsWithNoData": [
                          1
                        ]
                      }
                    ]
                  },
                  "Secondary": {
                    "Groupings": [
                      {
                        "Projections": [
                          2
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Key Measures",
                      "Name": "t"
                    },
                    {
                      "Entity": "Date",
                      "Name": "d"
                    },
                    {
                      "Entity": "Source Table",
                      "Name": "s"
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
                          "Property": "Date"
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
                        "Property": "Notifications"
                      },
                      "Name": "Table.Epi Curve"
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
                      "Name": "Date.Date"
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

recovered_3_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Key Measures\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Recovered Cases\"},\"Name\":\"Table.Cases Cleared\"}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0]}]},\"DataReduction\":{\"DataVolume\":3,\"Primary\":{\"Top\":{}}},\"Version\":1}}}]}",
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
                      "Entity": "Key Measures",
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
                        "Property": "Recovered Cases"
                      },
                      "Name": "Table.Cases Cleared"
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


regions_exact_2_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"t\",\"Entity\":\"Key Measures\"},{\"Name\":\"s\",\"Entity\":\"Shape Map(SA3)\"}],\"Select\":[{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"},\"Name\":\"Table.Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"SA3\"},\"Name\":\"Shape Map(SA3).SA3\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Confirmed Cases\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Top\":{}}},\"Aggregates\":[{\"Select\":0,\"Aggregations\":[{\"Min\":{}},{\"Max\":{}}]}],\"Version\":1}}}]}",
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
                      "Select": 0
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
                      "Entity": "Key Measures",
                      "Name": "t"
                    },
                    {
                      "Entity": "Shape Map(SA3)",
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
                          "Property": "Confirmed Cases"
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
                        "Property": "Confirmed Cases"
                      },
                      "Name": "Table.Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "s"
                          }
                        },
                        "Property": "SA3"
                      },
                      "Name": "Shape Map(SA3).SA3"
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


age_groups_6_req = {
        "ApplicationContext": {
          "DatasetId": "3a1dc16f-89aa-4e71-b1f1-0e2e2b04aa42",
          "Sources": [
            {
              "ReportId": "6b564b1a-20ea-4707-826f-04a750b77678"
            }
          ]
        },
        "CacheKey": "{\"Commands\":[{\"SemanticQueryDataShapeCommand\":{\"Query\":{\"Version\":2,\"From\":[{\"Name\":\"a1\",\"Entity\":\"Age Buckets\"},{\"Name\":\"t\",\"Entity\":\"Table\"},{\"Name\":\"c\",\"Entity\":\"COVID%20Case%20Data%20(02042020)\"}],\"Select\":[{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"},\"Name\":\"Age Buckets (2).Age Group\"},{\"Measure\":{\"Expression\":{\"SourceRef\":{\"Source\":\"t\"}},\"Property\":\"Count of Confirmed Cases\"},\"Name\":\"Table.Count of Confirmed Cases\"},{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"c\"}},\"Property\":\"Sex\"},\"Name\":\"COVID%20Case%20Data%20(02042020).Sex\"}],\"OrderBy\":[{\"Direction\":1,\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"a1\"}},\"Property\":\"Age group (years)\"}}}]},\"Binding\":{\"Primary\":{\"Groupings\":[{\"Projections\":[0,1]}]},\"Secondary\":{\"Groupings\":[{\"Projections\":[2]}]},\"DataReduction\":{\"DataVolume\":4,\"Primary\":{\"Window\":{\"Count\":200}},\"Secondary\":{\"Top\":{\"Count\":60}}},\"Version\":1}}}]}",
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
                          1
                        ]
                      }
                    ]
                  },
                  "Secondary": {
                    "Groupings": [
                      {
                        "Projections": [
                          2
                        ]
                      }
                    ]
                  },
                  "Version": 1
                },
                "Query": {
                  "From": [
                    {
                      "Entity": "Age Buckets",
                      "Name": "a1"
                    },
                    {
                      "Entity": "Table",
                      "Name": "t"
                    },
                    {
                      "Entity": "COVID%20Case%20Data%20(02042020)",
                      "Name": "c"
                    }
                  ],
                  "OrderBy": [
                    {
                      "Direction": 1,
                      "Expression": {
                        "Column": {
                          "Expression": {
                            "SourceRef": {
                              "Source": "a1"
                            }
                          },
                          "Property": "Age group (years)"
                        }
                      }
                    }
                  ],
                  "Select": [
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "a1"
                          }
                        },
                        "Property": "Age group (years)"
                      },
                      "Name": "Age Buckets (2).Age Group"
                    },
                    {
                      "Measure": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "t"
                          }
                        },
                        "Property": "Count of Confirmed Cases"
                      },
                      "Name": "Table.Count of Confirmed Cases"
                    },
                    {
                      "Column": {
                        "Expression": {
                          "SourceRef": {
                            "Source": "c"
                          }
                        },
                        "Property": "Sex"
                      },
                      "Name": "COVID%20Case%20Data%20(02042020).Sex"
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
    apb = ACTPowerBI()
    apb.run_powerbi_grabber()

