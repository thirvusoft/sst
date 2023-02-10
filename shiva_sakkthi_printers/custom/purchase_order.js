frappe.ui.form.on("Purchase Order", {
    refresh: function (frm) {
        frm.set_value("letter_head", "Shivasakthi PO letterhead tax invoice")
    },
    before_save: function (frm) {
        frm.set_value("letter_head", "Shivasakthi PO letterhead tax invoice")
    },
    onload_post_render: function (frm) {
        frm.set_value("letter_head", "Shivasakthi PO letterhead tax invoice")
    }
})