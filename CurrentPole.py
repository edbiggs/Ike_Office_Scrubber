class CurrentPole():

    class Equipment():
        def __init__(self):
            self.equipment_type = None
            self.equipment_orientation = None
            self.equipment_attachment_height_ft = None
            self.equipment_attachment_height_in = None

    class Anchor():

        class Guy():
            def __init__(self):
                self.guy_size = None
                self.guy_attachment_height_ft = None
                self.guy_attachment_height_in = None

        def __init__(self):
            self.anchor_lead_length_ft = None
            self.anchor_lead_length_in = None
            self.anchor_lead_orientation = None
            # Each Guy instance attached dynamically as guy_1, guy_2, ...

    class Span():

        class PowerCircuit():
            def __init__(self):
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

        def __init__(self):
            self.span_length = None
            self.span_type = None
            self.span_mid_span_ike_photo = None
            # PowerCircuit instances attached dynamically as power_circuit_1, ...
            # Communication instances attached dynamically as communication_1, ...

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
        self.guys = None
        self.anchor_subsection_count = None
        self.ms_height = None
        self.ms_clearance = None
        # Equipment instances attached dynamically as equipment_1, equipment_2, ...
        # Anchor instances attached dynamically as anchor_1, anchor_2, ...
        # Span instances attached dynamically as span_1, span_2, ...
