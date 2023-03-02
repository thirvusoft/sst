<template>
  <v-row justify="center">
    <v-dialog v-model="customerDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="headline primary--text">{{ __('Customer Info') }}</span>
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
                  readonly
                  v-model="customer_info.name"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Email')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.email_id"
                  @change="set_customer_info('email_id', $event)"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('Mobile No')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.mobile_no"
                  @change="set_customer_info('mobile_no', $event)"
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
                  v-model="customer_info.ts_address_line_1"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('City')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.ts_city"
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
                  v-model="customer_info.ts_tax_category"
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
                  v-model="customer_info.ts_district"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('GSTIN')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.ts_gstin"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  dense
                  color="primary"
                  :label="frappe._('State')"
                  background-color="white"
                  hide-details
                  v-model="customer_info.ts_state"
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
                  v-model="customer_info.ts_gst_state"
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
                  v-model="customer_info.ts_pincode"
                ></v-text-field>
              </v-col>
              <!-- <v-col cols="6">
                <v-text-field
                  v-model="customer_info.loyalty_program"
                  :label="frappe._('Loyalty Program')"
                  dense
                  readonly
                  hide-details
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model="customer_info.loyalty_points"
                  :label="frappe._('Loyalty Points')"
                  dense
                  readonly
                  hide-details
                ></v-text-field>
              </v-col> -->
              <!-- End -->
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="error" dark @click="close_dialog">Close</v-btn>
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
    customer_info: '',
    // Customized By Thirvusoft
    // Start
    ts_tax_categorys: [],
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
  }),

  watch: {
    customer() {
      this.fetch_customer_details();
    },
  },

  methods: {
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
    close_dialog() {
      this.customerDialog = false;
    },

    set_customer_info(field, value) {
      const vm = this;
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.set_customer_info',
        args: {
          fieldname: field,
          customer: this.customer_info.name,
          value: value,
        },
        callback: (r) => {
          if (!r.exc) {
            vm.customer_info[field] = value;
            evntBus.$emit('show_mesage', {
              text: __('Customer contact updated successfully.'),
              color: 'success',
            });
            frappe.utils.play_sound('submit');
          }
        },
      });
    },
  },
  created: function () {
    evntBus.$on('open_edit_customer', () => {
      this.customerDialog = true;
    });
    evntBus.$on('set_customer_info_to_edit', (data) => {
      this.customer_info = data;
    });
    // Customized By Thirvusoft
    // Start
    this.getTaxCategory();
    // End
  },
};
</script>
