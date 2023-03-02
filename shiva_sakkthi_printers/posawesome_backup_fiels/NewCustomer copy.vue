<template>
  <v-row justify="center">
    <v-dialog v-model="customerDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline primary--text">{{ __('New Customer') }}</span>
        </v-card-title>
        <v-card-text class="pa-0">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Customer Name')"
                  background-color="white"
                  hide-details
                  v-model="customer_name"
                ></v-text-field>
              </v-col>
              <!-- <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Tax ID')"
                  background-color="white"
                  hide-details
                  v-model="tax_id"
                ></v-text-field>
              </v-col> -->
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Mobile No')"
                  background-color="white"
                  hide-details
                  v-model="mobile_no"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Email Id')"
                  background-color="white"
                  hide-details
                  v-model="email_id"
                ></v-text-field>
              </v-col>
              <!-- Customized By Thirvusoft
              Start -->
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Address Line')"
                  background-color="white"
                  hide-details
                  v-model="ts_address_line_1"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('City')"
                  background-color="white"
                  hide-details
                  v-model="ts_city"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  color="primary"
                  :label="frappe._('Tax Category')"
                  background-color="white"
                  hide-details
                  v-model="ts_tax_category"
                  :items="ts_tax_categorys"
                ></v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('District')"
                  background-color="white"
                  hide-details
                  v-model="ts_district"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('GSTIN')"
                  background-color="white"
                  hide-details
                  v-model="ts_gstin"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('State')"
                  background-color="white"
                  hide-details
                  v-model="ts_state"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  color="primary"
                  :label="frappe._('GST State')"
                  background-color="white"
                  hide-details
                  v-model="ts_gst_state"
                  :items="ts_gst_states"
                ></v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Pincode')"
                  background-color="white"
                  hide-details
                  v-model="ts_pincode"
                ></v-text-field>
              </v-col>
              <!-- <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Referral Code')"
                  background-color="white"
                  hide-details
                  v-model="referral_code"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-menu
                  ref="birthday_menu"
                  v-model="birthday_menu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  dense
                >
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field
                      v-model="birthday"
                      :label="frappe._('Birthday')"
                      readonly
                      dense
                      clearable
                      hide-details
                      v-bind="attrs"
                      v-on="on"
                      color="primary"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="birthday"
                    color="primary"
                    no-title
                    scrollable
                    :max="frappe.datetime.now_date()"
                    @input="birthday_menu = false"
                  >
                  </v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="primary"
                  :label="frappe._('Customer Group')"
                  v-model="group"
                  :items="groups"
                  background-color="white"
                  :no-data-text="__('Group not found')"
                  hide-details
                >
                </v-autocomplete>
              </v-col>
              <v-col cols="6">
                <v-autocomplete
                  clearable
                  dense
                  auto-select-first
                  color="primary"
                  :label="frappe._('Territory')"
                  v-model="territory"
                  :items="territorys"
                  background-color="white"
                  :no-data-text="__('Territory not found')"
                  hide-details
                >
                </v-autocomplete>
              </v-col> -->
              <!-- End -->
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
  </v-row>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    customerDialog: false,
    pos_profile: '',
    customer_name: '',
    tax_id: '',
    mobile_no: '',
    email_id: '',
    // Customized By Thirvusoft
    // Start
    ts_address_line_1: '',
    ts_city: '',
    ts_tax_category: '',
    ts_tax_categorys: [],
    ts_district: '',
    ts_gstin: '',
    ts_state: '',
    ts_gst_state: '',
    ts_pincode: '',
    ts_gst_states : [
      "Andaman and Nicobar Islands",
      "Andhra Pradesh",
      "Arunachal Pradesh",
      "Assam",
      "Bihar",
      "Chandigarh",
      "Chhattisgarh",
      "Dadra and Nagar Haveli and Daman and Diu",
      "Delhi",
      "Goa",
      "Gujarat",
      "Haryana",
      "Himachal Pradesh",
      "Jammu and Kashmir",
      "Jharkhand",
      "Karnataka",
      "Kerala",
      "Ladakh",
      "Lakshadweep Islands",
      "Madhya Pradesh",
      "Maharashtra",
      "Manipur",
      "Meghalaya",
      "Mizoram",
      "Nagaland",
      "Odisha",
      "Other Territory",
      "Pondicherry",
      "Punjab",
      "Rajasthan",
      "Sikkim",
      "Tamil Nadu",
      "Telangana",
      "Tripura",
      "Uttar Pradesh",
      "Uttarakhand",
      "West Bengal"
    ],
    // End
    referral_code: '',
    birthday: null,
    birthday_menu: false,
    group: '',
    groups: [],
    territory: '',
    territorys: [],
  }),
  watch: {},
  methods: {
    close_dialog() {
      this.customerDialog = false;
    },
    getCustomerGroups() {
      if (this.groups.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Customer Group', {
          fields: ['name'],
          page_length: 1000,
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.groups.push(el.name);
            });
          }
        });
    },
    getCustomerTerritorys() {
      if (this.territorys.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Territory', {
          fields: ['name'],
          page_length: 1000,
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.territorys.push(el.name);
            });
          }
        });
    },
    // Customized By Thirvusoft
    // Start
    getTaxCategory(){
      if (this.ts_tax_categorys.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Tax Category', {
          fields: ['name'],
          page_length: 1000,
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.ts_tax_categorys.push(el.name);
            });
          }
        });
    },
    // End
    submit_dialog() {
      if (this.customer_name) {
        // Customized By Thirvusoft
        // Start
        if (this.ts_address_line_1){
          if (this.ts_city){
            if (this.ts_district){
              if (this.ts_gstin){
                if (this.ts_gst_state){
                  if (this.ts_state){
                    if (this.ts_pincode){
                      const vm = this;
                      const args = {
                        customer_name: this.customer_name,
                        company: this.pos_profile.company,
                        tax_id: this.tax_id,
                        mobile_no: this.mobile_no,
                        email_id: this.email_id,

                        ts_address_line_1: this.ts_address_line_1,
                        ts_city: this.ts_city,
                        ts_tax_category: this.ts_tax_category,
                        ts_district: this.ts_district,
                        ts_gstin: this.ts_gstin,
                        ts_state: this.ts_state,
                        ts_gst_state: this.ts_gst_state,
                        ts_pincode: this.ts_pincode,

                        referral_code: this.referral_code,
                        birthday: this.birthday,
                        customer_group: this.group,
                        territory: this.territory,
                      };
                      frappe.call({
                        method: 'posawesome.posawesome.api.posapp.create_customer',
                        args: args,
                        callback: (r) => {
                          if (!r.exc && r.message.name) {
                            evntBus.$emit('show_mesage', {
                              text: __('Customer contact created successfully.'),
                              color: 'success',
                            });
                            args.name = r.message.name;
                            frappe.utils.play_sound('submit');
                            evntBus.$emit('add_customer_to_list', args);
                            evntBus.$emit('set_customer', r.message.name);
                            vm.customer_name = '';
                            vm.tax_id = '';
                            vm.mobile_no = '';
                            vm.email_id = '';
                          
                            vm.ts_address_line_1 = '';
                            vm.ts_city = '';
                            vm.ts_tax_category = '';
                            vm.ts_district = '';
                            vm.ts_gstin = '';
                            vm.ts_state = '';
                            vm.ts_gst_state = '';
                            vm.ts_pincode = '';
              
                            vm.referral_code = '';
                            vm.birthday = '';
                            vm.group = '';
                            vm.customerDialog = false;
                          }
                        },
                      });
                      this.customerDialog = false;
                    }
                    else{
                      evntBus.$emit('show_mesage', {
                          text: `Please Type The Pincode`,
                          color: 'error',
                        });
                    }
                  }
                  else{
                    evntBus.$emit('show_mesage', {
                        text: `Please Type The State`,
                        color: 'error',
                      });
                  }
                }
                else{
                  evntBus.$emit('show_mesage', {
                      text: `Please Type The GST State`,
                      color: 'error',
                    });
                }
              }
              else{
                evntBus.$emit('show_mesage', {
                    text: `Please Type The GSTIN`,
                    color: 'error',
                  });
              }
            }
            else{
              evntBus.$emit('show_mesage', {
                text: `Please Type The District`,
                color: 'error',
              });
            }
          }
          else{
            evntBus.$emit('show_mesage', {
              text: `Please Type The City`,
              color: 'error',
            });
         }
        }
        else{
          evntBus.$emit('show_mesage', {
            text: `Please Type The Address Line`,
            color: 'error',
          });
        }
      }
      else{
        evntBus.$emit('show_mesage', {
          text: `Please Type The Customer Name`,
          color: 'error',
        });
      }
      // End
    },
  },
  created: function () {
    evntBus.$on('open_new_customer', () => {
      this.customerDialog = true;
    });
    evntBus.$on('register_pos_profile', (data) => {
      this.pos_profile = data.pos_profile;
    });
    this.getCustomerGroups();
    this.getCustomerTerritorys();
    // Customized By Thirvusoft
    // Start
    this.getTaxCategory();
    // End
  },
};
</script>