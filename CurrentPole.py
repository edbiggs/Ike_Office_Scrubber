class CurrentPole():
    def __init__(self, pole_id):
        self.pole_id = pole_id
        self.pole_type = None
        self.tip = None
        self.latitude = None
        self.longitude = None
        self.pla_result = None
        self.pole_tag = None
        self.facility_id_slider = None
        self.facility_id_text = None
        self.mf_hdw = None
        self.anchor_count = None
        self.riser_count = None
        self.splice_point_slider = None
        self.splice_type = None
        self.slack_loop = None
        self.storage_type = None
        self.strand = None
        self.vault = None
        self.equipment_subform_count = None
        self.anchor_subform_count = None
        self.span_subform_count = None

    class Equipment():
        def __init__(self):
            self.equipment_type = None
            self.equipment_orientation = None
            self.equipment_attachment_height_ft = None
            self.equipment_attachment_height_in = None

    class Anchor():
        def __init__(self):
            self.anchor_lead_length_ft = None
            self.anchor_lead_length_in = None
            self.anchor_lead_orientation = None

        class Guy():
            def __init__(self):
                self.guy_subform_count = None
                self.guy_size = None
                self.guy_attachment_height_ft = None
                self.guy_attachment_height_in = None

    class Span():
        def __init__(self):
            self.span_length = None
            self.span_type = None
            self.span_mid_span_ike_photo = None

        class PowerCircuit():
            def __init__(self):
                self.power_circuit_subform_count = None
                self.power_circuit_type = None
                self.power_circuit_primary_conductor = None
                self.power_circuit_primary_framing = None
                self.power_circuit_primary_phase_a_height_ft = None
                self.power_circuit_primary_phase_a_height_in = None
                self.power_circuit_primary_phase_b_height_ft = None
                self.power_circuit_primary_phase_b_height_in = None
                self.power_circuit_primary_phase_c_height_ft = None
                self.power_circuit_primary_phase_c_height_in = None
                self.power_circuit_neutral_conductor = None
                self.power_circuit_neutral_framing = None
                self.power_circuit_neutral_height_ft = None
                self.power_circuit_neutral_height_in = None

        class Communication():
            def __init__(self):
                self.communication_subform_count = None
                self.communication_mid_span_height = None
                self.communication_size = None
                self.communication_owner = None
                self.communication_horizontal_offset = None
                self.communication_attachment_height = None
                self.communication_attachment_height_ft = None
                self.communication_attachment_height_in = None
                self.communication_ms_clearance = None
                self.communication_midspan_ike_photo = None
                self.communication_joint_use = None



poles_dict = {
    "pole id": [],
    "main": {
        "pole type": [],
        "tip": [],
        "latitude": [],
        "longitude": [],
        "pla_result": [],
        "pole_tag": [],
        "facility_id_slider": [],
        "facility_id_text": [],
        "mf_hdw": [],
        "anchor_count": [],
        "riser_count": [],
        "splice_point_slider": [],
        "splice_type": [],
        "slack_loop": [],
        "storage_type": [],
        "strand": [],
        "vault": [],
        "equipment_subform_count": [],
        "anchor_subform_count": [],
        "span_subform_count": []
        },
    "equipment": {
        "equipment_type": [],
        "equipment_orientation": [],
        "equipment_attachment_height_ft": [],
        "equipment_attachment_height_in": []
    },
    "anchor": {
        "anchor_lead_length_ft": [],
        "anchor_lead_length_in": [],
        "anchor_lead_orientation": [],

        "guy": {
            "guy_subform_count": [],
            "guy_size": [],
            "guy_attachment_height_ft": [],
            "guy_attachment_height_in": []
        }
    },
    "span": {
        "span_length": [],
        "span_type": [],
        "span_mid_span_ike_photo": [],

        "power circuit": {
            "power_circuit_subform_count": [],
            "power_circuit_type": [],
            "power_circuit_primary_conductor": [],
            "power_circuit_primary_framing": [],
            "power_circuit_primary_phase_a_height_ft": [],
            "power_circuit_primary_phase_a_height_in": [],
            "power_circuit_primary_phase_b_height_ft": [],
            "power_circuit_primary_phase_b_height_in": [],
            "power_circuit_primary_phase_c_height_ft": [],
            "power_circuit_primary_phase_c_height_in": [],
            "power_circuit_neutral_conductor": [],
            "power_circuit_neutral_framing": [],
            "power_circuit_neutral_height_ft": [],
            "power_circuit_neutral_height_in": []
        },
        "communication": {
            "communication_subform_count": [],
            "communication_mid_span_height": [],
            "communication_size": [],
            "communication_owner": [],
            "communication_horizontal_offset": [],
            "communication_attachment_height": [],
            "communication_attachment_height_ft": [],
            "communication_attachment_height_in": [],
            "communication_ms_clearance": [],
            "communication_midspan_ike_photo": [],
            "communication_joint_use": []
        }
    }
}

