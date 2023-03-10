<template>
    <v-row justify="center">
        <v-dialog v-model="CustomerLedgerDialog" max-width="450px">
            <v-card>
                <v-card-title>
                    <span class="headline primary--text">{{ __('Customer Ledger') }}</span>
                </v-card-title>
                <v-card-text class="pa-0">
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-autocomplete
                                    clearable
                                    dense
                                    outlined
                                    color="primary"
                                    :label="frappe._('Customer')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_customer"
                                    :items="ts_customers"
                                ></v-autocomplete>
                            </v-col>
                        </v-row>
                        <v-row>
                            <v-col>
                                <v-menu
                                    ref="ts_from_dates"
                                    v-model="ts_from_dates"
                                    :close-on-content-click="false"
                                    transition="scale-transition"
                                    dense
                                    >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field style="top: 8px;"
                                            v-model="ts_from_date"
                                            ref = "ts_from_date"
                                            :label="frappe._('From Date')"
                                            dense
                                            outlined
                                            clearable
                                            hide-details
                                            v-bind="attrs"
                                            v-on="on"
                                            color="primary"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="ts_from_date"
                                        color="primary"
                                        no-title
                                        scrollable
                                        @input="ts_from_dates = false"
                                    >
                                    </v-date-picker>
                                </v-menu>
                            </v-col>
                            <v-col>
                                <v-menu
                                    ref="ts_to_dates"
                                    v-model="ts_to_dates"
                                    :close-on-content-click="false"
                                    transition="scale-transition"
                                    dense
                                    >
                                    <template v-slot:activator="{ on, attrs }">
                                        <v-text-field style="top: 8px;"
                                            v-model="ts_to_date"
                                            ref = "ts_to_date"
                                            :label="frappe._('To Date')"
                                            dense
                                            outlined
                                            clearable
                                            hide-details
                                            v-bind="attrs"
                                            v-on="on"
                                            color="primary"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="ts_to_date"
                                        color="primary"
                                        no-title
                                        scrollable
                                        @input="ts_to_dates = false"
                                    >
                                    </v-date-picker>
                                </v-menu>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn color="error" dark @click="close_dialog">{{
                            __('Close')
                        }}</v-btn>
                        <v-btn color="success" dark @click="submit_dialog">{{
                            __('Submit')
                        }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="CustomerLedgerTableDialog" max-width="600px">
            <v-card>
                <v-card-text class="pa-0">
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-col cols="12">
                                    <v-autocomplete
                                        dense
                                        outlined
                                        readonly
                                        color="primary"
                                        :label="frappe._('Customer')"
                                        background-color="white"
                                        hide-details
                                        v-model="ts_customer"
                                        :items="ts_customers"
                                    ></v-autocomplete>
                                </v-col>
                                <v-row>
                            <v-col>
                                <v-text-field style="top: 8px;"
                                    v-model="ts_from_date"
                                    ref = "ts_from_date"
                                    :label="frappe._('From Date')"
                                    dense
                                    outlined
                                    readonly
                                    hide-details
                                    color="primary"
                                ></v-text-field>
                            </v-col>
                            <v-col>
                                <v-text-field style="top: 8px;"
                                    v-model="ts_to_date"
                                    :label="frappe._('To Date')"
                                    dense
                                    outlined
                                    readonly
                                    hide-details
                                    color="primary"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                            <v-data-table
                                :headers="items_headers"
                                :items="items_invoice_no_value"
                                outlined
                                item-key="posa_row_id"
                                class="elevation-1"
                                :items-per-page="itemsPerPage"
                                hide-default-footer
                            >
                            <template v-slot:item.invoice_no="{ item }">
                                <v-text-field
                                    dense
                                    outlined
                                    readonly
                                    color="primary"
                                    background-color="white"
                                    hide-details
                                    v-model="item.invoice_no"
                                ></v-text-field>
                            </template>
                            <template v-slot:item.value="{ item }">
                                <v-text-field
                                    dense
                                    outlined
                                    readonly
                                    color="primary"
                                    background-color="white"
                                    hide-details
                                    v-model="item.value"
                                ></v-text-field>
                            </template>
                        </v-data-table>
                        </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="accent" dark @click="table_back_dialog">{{
                    __('Back')
                    }}</v-btn>
                    <v-btn color="error" dark @click="table_close_dialog">{{
                    __('Close')
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
        ts_customer: '',
        ts_customers: [],
        CustomerLedgerDialog : false,
        CustomerLedgerTableDialog: false,
        ts_from_date: '',
        ts_from_dates: false,
        ts_to_date: '',
        ts_to_dates: false,

        sizeDialog: false,
        itemsPerPage: 1000,
        
        items_headers: [
        { text: __('Invoice No'), value: 'invoice_no', align: 'center' },
        { text: __('Value'), value: 'value', align: 'center' },
        ],

        items_invoice_no_value: [],
    }),
    watch: {},
    methods: {
        table_close_dialog (){
            this.ts_customer = '';
            this.ts_from_date = '';
            this.ts_to_date =  '';
            this.CustomerLedgerDialog = false;
            this.items_invoice_no_value = [];
            this.CustomerLedgerTableDialog = false;
        },

        table_back_dialog (){
            this.CustomerLedgerTableDialog = false;
        },

        table_value (){
            const vm = this;
            const args = {
                ts_customer : this.ts_customer,
                ts_from_date : this.ts_from_date,
                ts_to_date : this.ts_to_date
            };
            frappe.call({
                method: 'posawesome.posawesome.api.posapp.get_customer_ledger',
                args: args,

                callback: function (r) {
                    if (r.message) {
                        
                        vm.items_invoice_no_value = r.message;
                        vm.CustomerLedgerTableDialog = true;

                    }
                },
            });
        },

        submit_dialog (){
            if(this.ts_customer){
                if(this.ts_from_date){

                    if(this.ts_to_date){
                        this.table_value()
                    }

                    else{
                        evntBus.$emit('show_mesage', {
                            text: `Please Select The To Date`,
                            color: 'error',
                        });
                    }
                }

                else{
                    evntBus.$emit('show_mesage', {
                        text: `Please Select The From Date`,
                        color: 'error',
                    });
                }
            }

            else{
                evntBus.$emit('show_mesage', {
                    text: `Please Select The Customer`,
                    color: 'error',
                });
            }
        },

        close_dialog (){

            this.ts_customer = '';
            this.ts_from_date = '';
            this.ts_to_date =  '';
            this.CustomerLedgerDialog = false;
        },

        
        get_customer_names() {

            const vm = this;

            frappe.call({
                method: 'posawesome.posawesome.api.posapp.ts_get_customer_names',
                args: {},

                callback: function (r) {
                    if (r.message) {

                        vm.ts_customers = r.message;
                    }
                },
            });
        },
    },
    created: function () {
        evntBus.$on('CustomerLedger', () => {
            this.CustomerLedgerDialog = true;
        });

        this.get_customer_names();
    },
  };
  </script>