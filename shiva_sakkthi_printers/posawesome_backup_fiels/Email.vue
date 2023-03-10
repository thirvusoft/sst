<template>
    <v-row justify="center">
        <v-dialog v-model="CheckEmail" max-width="400px">
            <v-card>
                <v-card-title>
                    <span class="headline primary--text">{{ __('Do you want to send the mail?') }}</span>
                </v-card-title>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="error" dark @click="close_dialog">{{
                        __('No')
                    }}</v-btn>
                    <v-btn color="success" dark @click="submit_dialog">{{
                        __('Yes')
                    }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="EmailCreation" max-width="500px">
            <v-card>
                <v-card-title>
                    <span class="headline primary--text">{{ __('Email') }}</span>
                </v-card-title>
                <v-card-text class="pa-0">
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    dense
                                    color="primary"
                                    :label="frappe._('Email ID')"
                                    background-color="white"
                                    hide-details
                                    outlined
                                    clearable
                                    v-model="ts_email_id"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    dense
                                    outlined
                                    readonly
                                    color="primary"
                                    :label="frappe._('Invoice No')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_invoice_no"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    dense
                                    outlined
                                    color="primary"
                                    :label="frappe._('Subject')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_subject"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="12">
                                <v-text-field
                                    dense
                                    outlined
                                    color="primary"
                                    :label="frappe._('Message')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_message"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn color="error" dark @click="close_dialog_email">{{
                            __('Close')
                        }}</v-btn>
                        <v-btn color="success" dark @click="submit_dialog_email">{{
                            __('Send')
                        }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
    </v-row>
  </template>
  
  <script>
  import { evntBus } from '../../bus';
  export default {
    data: () => ({
        ts_email_id: '',
        ts_invoice_no: '',
        ts_subject: '',
        ts_message: '',
        ts_print_format: '',
        CheckEmail : false,
        EmailCreation : false,
    }),
    watch: {},
    methods: {

        submit_dialog_email() {
            if (this.ts_email_id){
                const args = {
                    recipients: this.ts_email_id,
                    cc: null,
                    bcc: null,
                    subject: this.ts_subject,
                    content: this.ts_message,
                    doctype: "Sales Invoice",
                    name: this.ts_invoice_no,
                    send_email: 1,
                    print_html: null,
                    send_me_a_copy: null,
                    print_format: this.ts_print_format,
                    sender: "shivasakkthitransfer@gmail.com",
                    sender_full_name: "SHIVA SAKKTHI TRANSFER",
                    email_template: null,
                    attachments: "[]",
                    _lang : "English (United States)",
                    read_receipt:null,
                    print_letterhead: null,
                }
                const vm = this;
                frappe.call({
                    method: 'frappe.core.doctype.communication.email.make',
                    args: args,
                    callback: function (r) {
                        if (!r.exc) {
                            frappe.utils.play_sound("email");

                            vm.CheckEmail = false;
                            vm.EmailCreation = false;

                            evntBus.$emit('show_mesage', {
                                text: __('Mail Sent Successfully.'),
                                color: 'success',
                            });

                        }
                    }
                })
            }
            else{
                evntBus.$emit('show_mesage', {
                    text: __('Please Type The Email ID.'),
                    color: 'error',
                });
            }
        },

        close_dialog() {
            this.CheckEmail = false;
        },

        submit_dialog() {
            this.EmailCreation = true;
        },

        close_dialog_email() {
            this.CheckEmail = false;
            this.EmailCreation = false;
        }

    },
    created: function () {
        evntBus.$on('email_check', (ts_invoice_no, ts_print_format, ts_email_id) => {
            this.ts_email_id = ts_email_id
            this.ts_invoice_no = ts_invoice_no;
            this.ts_subject = "Sales Invoice: " + ts_invoice_no
            this.ts_print_format = ts_print_format;
            this.CheckEmail = true;
        });
    },
  };
  </script>