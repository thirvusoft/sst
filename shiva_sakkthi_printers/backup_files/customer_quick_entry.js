frappe.provide('frappe.ui.form');
// get_variant_fields, fields adding and fields value changes
frappe.ui.form.CustomerQuickEntryForm = frappe.ui.form.QuickEntryForm.extend({
	init: function(doctype, after_insert, init_callback, doc, force) {
		this._super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	},

	render_dialog: function() {
		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		this._super();
	},

	get_variant_fields: function() {
		var variant_fields = [{
			fieldtype: "Section Break",
			label: __("Primary Contact Details"),
			collapsible: 0
		},
		{
			label: __("Email Id"),
			fieldname: "email_id",
			fieldtype: "Data"
		},
		{
			fieldtype: "Column Break"
		},
		{
			label: __("Phone Number"),
			fieldname: "mobile_no",
			fieldtype: "Data"
		},
		{
			fieldtype: "Section Break",
			label: __("Primary Address Details"),
			collapsible: 0
		},
		{
			label: __("Address Line 1"),
			fieldname: "address_line1",
			fieldtype: "Data"
        },
        {
			label: __("Tax Category"),
			fieldname: "tax_category",
			fieldtype: "Link",
            options:"Tax Category"
        },
        {
			label: __("GSTIN"),
			fieldname: "gstin",
			fieldtype: "Data"
        },
		{
			label: __("GST State"),
			fieldname: "gst_state",
			fieldtype: "Select",
            options:"Andaman and Nicobar Islands\nAndhra Pradesh\nArunachal Pradesh\nAssam\nBihar\nChandigarh\nChhattisgarh\nDadra and Nagar Haveli and Daman and Diu\nDelhi\nGoa\nGujarat\nHaryana\nHimachal Pradesh\nJammu and Kashmir\nJharkhand\nKarnataka\nKerala\nLadakh\nLakshadweep Islands\nMadhya Pradesh\nMaharashtra\nManipur\nMeghalaya\nMizoram\nNagaland\nOdisha\nOther Territory\nPondicherry\nPunjab\nRajasthan\nSikkim\nTamil Nadu\nTelangana\nTripura\nUttar Pradesh\nUttarakhand\nWest Bengal"
        },
		{
			fieldtype: "Column Break"
		},
		{
			label: __("City"),
			fieldname: "city",
			fieldtype: "Data"
		},
        {
			label: __("District"),
			fieldname: "district",
			fieldtype: "Data"
		},
		{
			label: __("State"),
			fieldname: "state",
			fieldtype: "Data"
		},
        {
			label: __("Pincode"),
			fieldname: "pincode",
			fieldtype: "Data"
		},
        {
            label: __("Country"),
            fieldname: "country",
            fieldtype: "Link",
            options: "Country",
            hidden:1,
            default:"India"
        },
    ];

		return variant_fields;
	},
})
