xpath_map = {
        "main": {
            "fields": {
                "no_changes": {
                    "xpath": "//a[@title='No changes']",
                    "data type": "slider"
                    },
                    "pole_id": {
                        "xpath": "//div[@title='ID']"
                                    "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                        "data type": "value"
                    },
                    "pole_type": {
                        "xpath": "//div[@title='Type']"
                                    "[not(ancestor::div[contains(@class,'c-SubFormInstance')])]"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//span[contains(@class,'c-MultiListInput__label')]",
                        "data type": "text"
                    },
                    "tip": {
                        "xpath": "//div[@title='Tip']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                    "//input",
                        "data type": "value",
                    },
                    "latitude": {
                        "xpath": "//div[contains(@class,'c-Input--lat') and contains(@class,'is-dirty')]"
                                    "//input",
                        "data type": "value",
                    },
                    "longitude": {
                        "xpath": "//div[contains(@class,'c-Input--lng') and contains(@class,'is-dirty')]"
                                    "//input",
                        "data type": "value",
                    },
                    "pla_result": {
                        "xpath": "//div[@title='PLA Result']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//textarea",
                        "data type": "text",
                    },
                    "pole_tag": {
                        "xpath": "//div[@title='Pole Tag']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//input[contains(@class,'c-SwitchInput__input')]",
                        "data type": "slider",
                    },
                    "facility_id_slider": {
                        "xpath": "//div[@title='Facility ID']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//input[contains(@class,'c-SwitchInput__input')]",
                        "data type": "slider",
                    },
                    "facility_id_text": {
                        "xpath": "//div[@title='Facility ID Number']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                        "data type": "value",
                    },
                    "mf_hdw": {
                        "xpath": "//div[@title='M/F Hdw.']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                        "data type": "value",
                    },
                    "anchor_count": {
                        "xpath": "//div[@title='Anchor']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                        "data type": "value",
                    },
                    "riser_count": {
                        "xpath": "//div[@title='Riser']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                        "data type": "value",
                    },
                    "splice_point_slider": {
                        "xpath": "//div[@title='Splice Point']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//input[contains(@class,'c-SwitchInput__input')]",
                        "data type": "slider",
                    },
                    # Not verified
                    "splice_type": {
                        "xpath": "//div[@title='Splice Type']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                        "data type": "value",
                    },
                    "slack_loop": {
                        "xpath": "//div[@title='Slack Loop']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//input[contains(@class,'c-SwitchInput__input')]",
                        "data type": "slider",
                    },
                    "storage_type": {
                        "xpath": "//div[@title='Storage Type']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                        "data type": "value",
                    },
                    "strand": {
                        "xpath": "//div[@title='Strand']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//textarea",
                        "data type": "value",
                    },
                    "vault": {
                        "xpath": "//div[@title='Vault']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//input[contains(@class,'c-SwitchInput__input')]",
                        "data type": "slider",
                    },
                    "reel_id": {
                        "xpath": "//div[@title='Reel ID']"
                                    "/following-sibling::div[contains(@class, 'c-CollectionField__Value')]"
                                    "//textarea",
                        "data type": "value",
                    }
            },
        },
        "equipment": {
            "fields": {
                "equipment_count": {
                    "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Equipment']"
                            "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
                    "data type": "text"
                    },
                "equipment_type": {
                    "xpath": "//div[contains(@id,'ipf_equipmentType')]"
                                "//span[contains(@class,'c-MultiListInput__label')]",
                    "data type": "text"
                },
                "equipment_orientation": {
                    "xpath": "//div[contains(@id,'ipf_equipmentOrientation')]"
                                "//div[contains(@class,'c-Input--is-dirty')]"
                                "//input",
                    "data type": "value"
                },
                "equipment_attachment_height_ft": {
                    "xpath": "//div[contains(@id,'ipf_equipmentAttachmentHeight')]"
                                "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                "//input",
                    "data type": "value"
                },
                "equipment_attachment_height_in": {
                    "xpath": "//div[contains(@id,'ipf_equipmentAttachmentHeight')]"
                                "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                "//input",
                    "data type": "value"
                }
            },
        },
        "anchor": {
            "fields": {
                "anchor_count": {
                    "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Anchor']"
                                "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
                    "data type": "text"
                },
                "anchor_lead_length_ft": {
                    "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                                "//div[contains(@class,'c-VectorInput__leftInput')]"
                                "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                "//input",
                    "data type": "value"
                },
                "anchor_lead_length_in": {
                    "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                                "//div[contains(@class,'c-VectorInput__leftInput')]"
                                "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                "//input",
                    "data type": "value"
                },
                "anchor_lead_orientation": {
                    "xpath": "//div[contains(@id,'ipf_anchorLeadLength')]"
                                "//div[contains(@class,'c-Input--bearing') and contains(@class,'is-dirty')]"
                                "//input",
                    "data type": "value"
                }
            },
            "subforms": {
                "guys": {
                    "fields": {
                        "guys_count": {
                            "xpath": "//div[@title='Guys']"
                                    "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                    "//div[contains(@class,'is-dirty')]"
                                    "//textarea",
                            "data type": "value",
                            },
                            "guy_size": {
                                "xpath": "//div[contains(@id,'ipf_anchorGuySize')]"
                                        "//span[contains(@class,'c-MultiListInput__label')]",
                                "data type": "text"
                            },
                            "guy_attachment_height_ft": {
                                "xpath": "//div[contains(@id,'ipf_anchorGuyAttachmentHeight')]"
                                        "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                        "//input",
                                "data type": "value"
                            },
                            "guy_attachment_height_in": {
                                "xpath": "//div[contains(@id,'ipf_anchorGuyAttachmentHeight')]"
                                        "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                        "//input",
                                "data type": "value"
                            }
                    }                        
                }              
            }
        },
        "span": {
            "fields": {
                "span_count": {
                    "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Span']"
                            "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
                    "data type": "text",
                            },
                "span_length": {
                    "xpath": "//div[contains(@id,'ipf_spanLength')]"
                                "//div[contains(@class,'c-Input')]/span",
                    "data type": "text",
                },
                "span_type": {
                    "xpath": "//div[contains(@id,'ipf_spanType')]"
                                "//span[contains(@class,'c-MultiListInput__label')]",
                    "data type": "text",
                }
            },
            "subforms": {
                "power_circuit": {
                    "fields": {
                        "power_circuit_count": {
                            "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Power Circuit']"
                                        "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
                            "data type": "text",
                            },
                            "power_circuit_type": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitType')]"
                                            "//span[contains(@class,'c-MultiListInput__label')]",
                                "data type":"text",
                    
                            },
                            "power_circuit_primary_conductor": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryConductor')]"
                                            "//span[contains(@class,'c-MultiListInput__label')]",
                                "data type": "text",                                
                            },
                            "power_circuit_primary_framing": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryFraming')]"
                                            "//span[contains(@class,'c-MultiListInput__label')]",
                                "data type": "text",                                
                            },
                            "power_circuit_primary_phase_a_height_ft": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseAHeight')]"
                                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                                
                            },
                            "power_circuit_primary_phase_a_height_in": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseAHeight')]"
                                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                                
                            },
                            "power_circuit_primary_phase_b_height_ft": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseBHeight')]"
                                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                                
                            },
                            "power_circuit_primary_phase_b_height_in": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseBHeight')]"
                                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                                
                            },
                            "power_circuit_primary_phase_c_height_ft": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseCHeight')]"
                                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                                
                            },
                            "power_circuit_primary_phase_c_height_in": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitPrimaryPhaseCHeight')]"
                                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                                
                            },
                            "power_circuit_neutral_conductor": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralConductor')]"
                                            "//span[contains(@class,'c-MultiListInput__label')]",
                                "data type": "text",                                
                            },
                            "power_circuit_neutral_framing": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralFraming')]"
                                            "//span[contains(@class,'c-MultiListInput__label')]",
                                "data type": "text",                                
                            },
                            "power_circuit_neutral_height_ft": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralHeight')]"
                                            "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                                
                            },
                            "power_circuit_neutral_height_in": {
                                "xpath": "//div[contains(@id,'ipf_spanPowerCircuitNeutralHeight')]"
                                            "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                            "//input",
                                "data type": "value",                               
                            }
                    },
                        
                },
                "communication": {
                    "fields": {
                        "communication_count": {
                            "xpath": "//div[contains(@class,'c-SubForm__TitleName') and @title='Communication']"
                                        "/following-sibling::div[contains(@class,'c-SubForm__TitleCount')]",
                            "data type": "text",
                        },
                        "communication_mid_span_height": {
                            "xpath": "//div[contains(@id,'ipf_spanCommunicationMidSpanHeight')]"
                                        "//div[contains(@class,'c-PMLink')]",
                            "data type": "text",
                        
                        },
                        "communication_size": {
                            "xpath": "//div[contains(@id,'ipf_spanCommunicationSize')]"
                                        "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                        
                        },
                        "communication_owner": {
                            "xpath": "//div[contains(@id,'ipf_spanCommunicationOwner')]"
                                        "//span[contains(@class,'c-MultiListInput__label')]",
                            "data type": "text",
                        
                        },
                        "communication_horizontal_offset": {
                            "xpath": "//div[contains(@id,'ipf_spanCommunicationHorizOffset')]"
                                        "//div[contains(@class,'c-Input--is-dirty')]"
                                        "//input",
                            "data type": "value",
                        
                        },
                        "communication_attachment_height": {
                            "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                                        "//div[contains(@class,'c-PMLink') and not(contains(@class,'c-PMLink--inputs'))]",
                            "data type": "text",
                        
                        },
                        "communication_attachment_height_ft": {
                            "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                                        "//div[contains(@class,'c-Input--ft') and contains(@class,'is-dirty')]"
                                        "//input",
                            "data type": "value",
                        
                        },
                        "communication_attachment_height_in": {
                            "xpath": "//div[contains(@id,'ipf_spanCommunicationAttachmentHeight')]"
                                        "//div[contains(@class,'c-Input--in') and contains(@class,'is-dirty')]"
                                        "//input",
                            "data type": "value",
                        
                        },
                        "communication_ms_clearance": {
                            "xpath": "//div[@title='MS Clearance ']"
                                        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                        "//div[contains(@class,'c-PMLink')]",
                            "data type": "text",
                        
                        },
                        "communication_midspan_ike_photo": {
                            "xpath": "//div[@title='MidSpan IKE Photo']"
                                        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]",
                            "data type": "text",
                        
                        },
                        "communication_joint_use": {
                            "xpath": "//div[@title='Joint Use']"
                                        "/following-sibling::div[contains(@class,'c-CollectionField__Value')]"
                                        "//input[contains(@class,'c-SwitchInput__input')]",
                            "data type": "slider",
                        
                        },
                        "ms_height": {
                            "xpath": "//div[contains(@class,'c-SubFormInstance')]"
                                        "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
                                        "//div[@title='Mid Span Height']"
                                        "/following-sibling::div"
                                        "//div[contains(@class,'c-PMLink')]",
                            "data type": "text",
                        
                        },
                        "ms_clearance": {
                            "xpath": "//div[contains(@class,'c-SubFormInstance')]"
                                        "[.//span[contains(@class,'c-MultiListInput__label') and contains(text(),'Fiber')]]"
                                        "//div[@title='MS Clearance ']"
                                        "/following-sibling::div"
                                        "//div[contains(@class,'c-PMLink')]",
                            "data type": "text"                                               
                        }
                    }
                }                               
            }
        }
    }