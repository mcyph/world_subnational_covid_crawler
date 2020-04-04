# Steps to install (tested only on Ubuntu 18.04 LTS):
# 1. Extract browsermob-proxy-2.1.4-bin.zip from
#    https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4
#    to your home directory
# 2. run "sudo pip3 install browsermob-proxy selenium editdistance psutil"
# 3. Follow the steps at https://tecadmin.net/setup-selenium-chromedriver-on-ubuntu/
# 4. Run this script with "python3 grab.py"


import os
import time
import json
import psutil
import datetime
import editdistance
from os import makedirs
from os.path import dirname, expanduser
from browsermobproxy import Server
from selenium import webdriver


BROWSER_MOB_PROXY_LOC = expanduser(
    '~/browsermob-proxy-2.1.4-bin/'
    'browsermob-proxy-2.1.4/bin/'
    'browsermob-proxy'
)
GECKO_BROWSER_DIR = expanduser(
    '~/geckodriver-v0.26.0-linux64/'
)


def grab():
    # Destroy any previous instances of browsermob-proxy
    for proc in psutil.process_iter():
        #print(proc.name())
        if proc.name() in ("browsermob-proxy",
                           "browsermob-prox"):
            print("Killing proc:", proc.name())
            proc.kill()

    print("Creating Server...")
    server = Server(BROWSER_MOB_PROXY_LOC)
    server.start()
    time.sleep(1)

    print("Creating Proxy...")
    proxy = server.create_proxy(params={'port': 9770})
    time.sleep(1)

    print("Creating Selenium/Chrome...")
    args = [
        "--proxy-server=localhost:%s" % proxy.port,
        '--ignore-certificate-errors',
        '--disable-dev-shm-usage',

        '--disable-extensions',
        '--disable-gpu',
        '--no-sandbox',
        '--headless',
    ]
    chrome_options = webdriver.ChromeOptions()
    for arg in args:
        chrome_options.add_argument(arg)
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1400, 1050)

    proxy.new_har("file_name", options={'captureHeaders': True,
                                        'captureContent': True})

    driver.get("https://app.powerbi.com/view?r=eyJrIjoiODBmMmE3NWQt"
               "ZWNlNC00OWRkLTk1NjYtMjM2YTY1MjI2NzdjIiwidCI6ImMwZTA"
               "2MDFmLTBmYWMtNDQ5Yy05Yzg4LWExMDRjNGViOWYyOCJ9")

    for x in range(3):
        time.sleep(25)

        proxy.wait_for_traffic_to_stop(10, 60)

        # Go to the next page
        content = driver.find_element_by_css_selector(
            '.glyphicon.glyph-small.pbi-glyph-chevronrightmedium.middleIcon'
        )
        content.click()

    proxy.wait_for_traffic_to_stop(10, 60)

    r = []
    #print(proxy.har, dir(proxy.har))
    for ent in proxy.har['log']['entries']:
        req = ent['request']
        #print(req['url'])
        if req['url'] == 'https://wabi-australia-southeast-api.analysis.windows.net/' \
                         'public/reports/querydata':
            if not 'postData' in req:
                print("ignoring:", req)
                continue

            #print(req.keys())
            #print(ent.keys())
            #print(ent)
            #print(req['postData'])
            #print(ent['response'])
            #print()

            r.append((
                json.loads(req['postData']['text']),
                json.loads(ent['response']['content']['text'])
            ))

    server.stop()
    driver.quit()
    return r

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





OUTPUT_DIR = None


def match_grabbed_with_types():
    global OUTPUT_DIR
    if not OUTPUT_DIR:
        OUTPUT_DIR = _get_output_json_dir()

    r = []

    for post_data, content in grab():
        j_post_data = json.dumps(post_data['queries'], sort_keys=True)

        most_likely = None
        smallest_dist = 999999999
        for k, v in globals().items():
            if k.endswith('_req'):
                v = json.dumps(v['queries'], sort_keys=True)
                dist = editdistance.distance(j_post_data, v)
                if dist < smallest_dist:
                    smallest_dist = dist
                    most_likely = k[:-4]

        r.append((
            smallest_dist,
            most_likely,
            post_data,
            content
        ))

        prefix = (
            most_likely+'_unconfirmed'
            if smallest_dist
            else most_likely
        )

        if smallest_dist:
            prefix_suffix = 1
            while True:
                path = f'{OUTPUT_DIR}/{prefix}-{prefix_suffix}.json'
                if not os.path.exists(path):
                    break
                prefix_suffix += 1
        else:
            path = f'{OUTPUT_DIR}/{prefix}.json'

        with open(path, 'w',
                  encoding='utf-8',
                  errors='replace') as f:
            f.write(json.dumps(
                [post_data, content],
                indent=2,
                sort_keys=True
            ))
    return r


def _get_output_json_dir():
    time_format = datetime.datetime \
        .now() \
        .strftime('%Y_%m_%d')

    # Get a revision id
    x = 0
    revision_id = 1

    while True:
        if x > 1000:
            # This should never happen, but still..
            raise Exception()

        dir_ = os.path.expanduser(
            f'~/dev/covid_19_data/vic/powerbi/'
            f'{time_format}-{revision_id}'
        )
        if not os.path.exists(dir_):
            break

        revision_id += 1
        x += 1

    try:
        makedirs(dir_)
    except OSError:
        pass
    return dir_


def iter_cache_paths(prefix):
    pass


def get_latest_cache_path(prefix):
    pass


if __name__ == '__main__':
    from sys import path
    from os import environ, pathsep, system
    path.append(GECKO_BROWSER_DIR)
    environ["PATH"] += pathsep + GECKO_BROWSER_DIR
    system('killall browsermob-prox')

    #grab()
    for dist, most_likely, post_data, content in match_grabbed_with_types():
        print()
        print(f"{most_likely}: Distance of {dist}"+
              (" - non-zero distance means match is probably incorrect!"
               if dist
               else ""))
        print("POST Query:", json.dumps(post_data, indent=2, sort_keys=True))
        print("Response:", json.dumps(content, indent=2, sort_keys=True))
