<template>
    <v-row justify="center">
        <v-dialog v-model="ItemCreationDialog" max-width="600px">
            <v-card>
                <v-card-title>
                    <span class="headline primary--text">{{ __('New Item') }}</span>
                </v-card-title>
                <v-card-text class="pa-0">
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    dense
                                    color="primary"
                                    :label="frappe._('Item Name')"
                                    background-color="white"
                                    readonly
                                    hide-details
                                    v-model="ts_item_name"
                                ></v-text-field>
                            </v-col>
                            <v-col cols="6">
                                <v-autocomplete
                                    clearable
                                    dense
                                    color="primary"
                                    :label="frappe._('Category')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_category"
                                    :items="ts_categorys"
                                    append-icon="mdi-plus"
                                    @click:append="new_category"
                                    @change="item_name_creation()"
                                ></v-autocomplete>
                            </v-col>
                            <v-col cols="6">
                                <v-autocomplete
                                    clearable
                                    dense
                                    color="primary"
                                    :label="frappe._('Variant')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_variant"
                                    :items="ts_variants"
                                    append-icon="mdi-plus"
                                    @click:append="new_variant"
                                    @change="item_name_creation()"
                                ></v-autocomplete>
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
        <v-dialog v-model="VariantCreationDialog" max-width="300px">
            <v-card>
                <v-card-title>
                    <span class="headline primary--text">{{ __('New Variant') }}</span>
                </v-card-title>
                <v-card-text class="pa-0">
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    dense
                                    color="primary"
                                    :label="frappe._('Variant')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_variant_creation"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn color="error" dark @click="close_dialog_variant">{{
                            __('Close')
                        }}</v-btn>
                        <v-btn color="success" dark @click="submit_dialog_variant">{{
                            __('Submit')
                        }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-dialog v-model="CategoryCreationDialog" max-width="300px">
            <v-card>
                <v-card-title>
                    <span class="headline primary--text">{{ __('New Category') }}</span>
                </v-card-title>
                <v-card-text class="pa-0">
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field
                                    dense
                                    color="primary"
                                    :label="frappe._('Category')"
                                    background-color="white"
                                    hide-details
                                    v-model="ts_category_creation"
                                ></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                        <v-btn color="error" dark @click="close_dialog_category">{{
                            __('Close')
                        }}</v-btn>
                        <v-btn color="success" dark @click="submit_dialog_category">{{
                            __('Submit')
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
        ts_item_name: '',
        ts_category: '',
        ts_variant: '',
        ts_variant_creation: '',
        ts_categorys: [],
        ts_variants: [],
        ts_category_creation: '',
        ItemCreationDialog : false,
        VariantCreationDialog : false,
        CategoryCreationDialog : false
    }),
    watch: {},
    methods: {
        item_name_creation(){
            var ts_category_name = this.ts_category || ""
            var ts_variant_name = this.ts_variant || ""
            this.ts_item_name = ts_category_name + " " + ts_variant_name
        },
        
        close_dialog(){
            this.ItemCreationDialog = false
            this.ts_item_name = ""
            this.ts_category = ""
            this.ts_variant = ""
        },

        close_dialog_variant(){
            this.VariantCreationDialog = false
            this.ts_variant_creation = ''
        },

        submit_dialog_variant(){
            if (this.ts_variant_creation){
                const args = {
                    ts_value: this.ts_variant_creation,
                    ts_type: "Variant"
                };
                frappe.call({
                    method: 'posawesome.posawesome.api.posapp.create_variant_category',
                    args: args,
                    callback: (r) => {
                        if (!r.exc && r.message.name) {

                            this.VariantCreationDialog = false

                            this.ts_variants.push(r.message.name)
                            this.ts_variant = r.message.name
                            this.item_name_creation()
                            
                            frappe.utils.play_sound('submit');

                            evntBus.$emit('show_mesage', {
                            text: __('Created Successfully.'),
                            color: 'success',
                            });
                                                    
                            this.ts_variant_creation = ""
                        }
                    }
                })
            }
            // else{
            //     evntBus.$emit('show_mesage', {
            //         text: `Please Type The Variant`,
            //         color: 'error',
            //     });
            // }
        },

        close_dialog_category(){
            this.CategoryCreationDialog = false
            this.ts_category_creation = ''
        },

        submit_dialog_category(){
            if (this.ts_category_creation){
                const args = {
                    ts_value: this.ts_category_creation,
                    ts_type: "Category"
                };
                frappe.call({
                    method: 'posawesome.posawesome.api.posapp.create_variant_category',
                    args: args,
                    callback: (r) => {
                        if (!r.exc && r.message.name) {

                            this.CategoryCreationDialog = false

                            this.ts_categorys.push(r.message.name)
                            this.ts_category = r.message.name
                            this.item_name_creation()
                            
                            frappe.utils.play_sound('submit');

                            evntBus.$emit('show_mesage', {
                            text: __('Created Successfully.'),
                            color: 'success',
                            });

                            this.ts_category_creation = ""
                        }
                    }
                })
            }
            else{
                evntBus.$emit('show_mesage', {
                    text: `Please Type The Variant`,
                    color: 'error',
                });
            }
        },

        submit_dialog(){
            // if (this.ts_item_name){
                if (this.ts_category){
                    // if (this.ts_variant){
                        const args = {
                            ts_item_name: this.ts_item_name,
                            ts_category: this.ts_category,
                            ts_variant: this.ts_variant,
                        };
                        frappe.call({
                            method: 'posawesome.posawesome.api.posapp.create_item',
                            args: args,
                            callback: (r) => {
                                if (!r.exc && r.message.name) {

                                    this.ItemCreationDialog = false
                                    
                                    frappe.utils.play_sound('submit');

                                    evntBus.$emit('show_mesage', {
                                    text: __('Item Created Successfully.'),
                                    color: 'success',
                                    });
                                    
                                    evntBus.$emit('ts_update_items_details');
                                
                                    this.ts_item_name = ""
                                    this.ts_category = ""
                                    this.ts_variant = ""
                                    
                                }
                            }
                        })
                    // }
                    // else{
                    //     evntBus.$emit('show_mesage', {
                    //         text: `Please Type The Variant`,
                    //         color: 'error',
                    //     });
                    // }
                }
                else{
                    evntBus.$emit('show_mesage', {
                        text: `Please Type The Category`,
                        color: 'error',
                    });
                }
            // }
            // else{
            //     evntBus.$emit('show_mesage', {
            //         text: `Please Type The Item Name`,
            //         color: 'error',
            //     });
            // }
        },

        getVariant(){
            if (this.ts_variants.length > 0) return;
                const vm = this;
                frappe.db
                    .get_list('Variant', {
                    fields: ['name'],
                    page_length: 1000,
                    })
                    .then((data) => {
                    if (data.length > 0) {
                        data.forEach((el) => {
                        vm.ts_variants.push(el.name);
                    });
                }
            });
        },

        getCategory(){
            if (this.ts_categorys.length > 0) return;
                const vm = this;
                frappe.db
                    .get_list('Category', {
                    fields: ['name'],
                    page_length: 1000,
                    })
                    .then((data) => {
                    if (data.length > 0) {
                        data.forEach((el) => {
                        vm.ts_categorys.push(el.name);
                    });
                }
            });
        },

        new_category() {
            this.CategoryCreationDialog = true;
        },

        new_variant() {
            this.VariantCreationDialog = true;
        },

    },
    created: function () {
        evntBus.$on('open_new_item_creation', () => {
            this.ItemCreationDialog = true;
        });

        this.getVariant();
        this.getCategory();
    },
  };
  </script>