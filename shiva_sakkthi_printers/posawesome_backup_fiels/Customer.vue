<template>
  <div>
    <v-autocomplete
      dense
      clearable
      auto-select-first
      outlined
      color="primary"
      :label="frappe._('Customer')"
      v-model="customer"
      :items="customers"
      item-text="customer_name"
      item-value="name"
      background-color="white"
      :no-data-text="__('Customer not found')"
      hide-details
      :filter="customFilter"
      :disabled="readonly"
      append-icon="mdi-plus"
      @click:append="new_customer"
      prepend-inner-icon="mdi-account-edit"
      @click:prepend-inner="edit_customer"
    > 
      <template v-slot:item="data">
        <template>
          <v-list-item-content>
            <v-list-item-title
              class="primary--text subtitle-1"
              v-html="data.item.customer_name"
            ></v-list-item-title>
            <v-list-item-subtitle
              v-if="data.item.customer_name != data.item.name"
              v-html="`ID: ${data.item.name}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.tax_id"
              v-html="`TAX ID: ${data.item.tax_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.email_id"
              v-html="`Email: ${data.item.email_id}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.mobile_no"
              v-html="`Mobile No: ${data.item.mobile_no}`"
            ></v-list-item-subtitle>
            <v-list-item-subtitle
              v-if="data.item.primary_address"
              v-html="`Primary Address: ${data.item.primary_address}`"
            ></v-list-item-subtitle>
          </v-list-item-content>
        </template>
      </template>
    </v-autocomplete>
    <!-- Customized By Thirvusoft
    Start -->
    <v-row>
      <v-col>
        <v-text-field style="top: 8px;"
          outlined
          dense
          clearable
          color="primary"
          auto-grow
          rows="1"
          :label="frappe._('PO No.')"
          v-model="ts_po_no"
          ref = "ts_po_no"
          ></v-text-field>
      </v-col>
      <v-col>
        <v-menu
          ref="ts_po_date_menu"
          v-model="ts_po_date_menu"
          :close-on-content-click="false"
          transition="scale-transition"
          dense
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field style="top: 8px;"
              v-model="ts_po_date"
              ref = "ts_po_date"
              :label="frappe._('PO Date')"
              readonly
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
            v-model="ts_po_date"
            color="primary"
            no-title
            scrollable
            @input="ts_po_date_menu = false"
          >
          </v-date-picker>
        </v-menu>
      </v-col>
    </v-row>
    <!-- End -->
  </div>
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    pos_profile: '',
    customers: [],
    customer: '',
    readonly: false,
    // Customized By Thirvusoft
    // Start
    ts_po_no: '',
    ts_po_date: frappe.datetime.now_date(),
    ts_po_date_menu: false,
    // End
  }),

  methods: {
    get_customer_names() {
      const vm = this;
      if (vm.pos_profile.posa_local_storage && localStorage.customer_storage) {
        vm.customers = JSON.parse(localStorage.getItem('customer_storage'));
      }
      frappe.call({
        method: 'posawesome.posawesome.api.posapp.get_customer_names',
        args: {
          pos_profile: this.pos_profile.pos_profile,
        },
        callback: function (r) {
          if (r.message) {
            vm.customers = r.message;
            console.info('loadCustomers');
            if (vm.pos_profile.posa_local_storage) {
              localStorage.setItem('customer_storage', '');
              localStorage.setItem(
                'customer_storage',
                JSON.stringify(r.message)
              );
            }
          }
        },
      });
    },
    new_customer() {
      evntBus.$emit('open_new_customer');
    },
    edit_customer() {
      evntBus.$emit('open_edit_customer');
    },
    customFilter(item, queryText, itemText) {
      const textOne = item.customer_name
        ? item.customer_name.toLowerCase()
        : '';
      const textTwo = item.tax_id ? item.tax_id.toLowerCase() : '';
      const textThree = item.email_id ? item.email_id.toLowerCase() : '';
      const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : '';
      const textFifth = item.name.toLowerCase();
      const searchText = queryText.toLowerCase();

      return (
        textOne.indexOf(searchText) > -1 ||
        textTwo.indexOf(searchText) > -1 ||
        textThree.indexOf(searchText) > -1 ||
        textFour.indexOf(searchText) > -1 ||
        textFifth.indexOf(searchText) > -1
      );
    },
    // Customized By Thirvusoft
    // Start
    shortOpenCustomer: function shortOpenCustomer(e) {
      if (e.key === 'c' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        this.$refs.customer.focus();
      }
    },
    shortOpenPoNO: function shortOpenPoNO(e) {
      if (e.key === 'F2') {
        e.preventDefault();
        this.$refs.ts_po_no.focus();
      }
    },
    shortOpenPODate: function shortOpenPODate(e) {
      if (e.key === 'F3') {
        e.preventDefault();
        this.$refs.ts_po_date.focus();
      }
    },
    // End
  },

  computed: {},

  created: function () {
    this.$nextTick(function () {
      evntBus.$on('register_pos_profile', (pos_profile) => {
        this.pos_profile = pos_profile;
        this.get_customer_names();
      });
      evntBus.$on('set_customer', (customer) => {
        this.customer = customer;
      });
      evntBus.$on('add_customer_to_list', (customer) => {
        this.customers.push(customer);
      });
      evntBus.$on('set_customer_readonly', (value) => {
        this.readonly = value;
      });
      evntBus.$on('clear_ts_po_details', () => {
        this.ts_po_no = '';
        this.ts_po_date = frappe.datetime.now_date();
      });
    });
    // Customized By Thirvusoft
    // Start
    document.addEventListener('keydown', this.shortOpenCustomer.bind(this));
    document.addEventListener('keydown', this.shortOpenPoNO.bind(this));
    document.addEventListener('keydown', this.shortOpenPODate.bind(this));
    // End
  },
  // Customized By Thirvusoft
  // Start
  destroyed: function destroyed() {
    document.removeEventListener('keydown', this.shortOpenCustomer);
    document.removeEventListener('keydown', this.shortOpenPoNO);
    document.removeEventListener('keydown', this.shortOpenPODate);
  },
  // End

  watch: {
    customer() {
      evntBus.$emit('update_customer', this.customer);
    },
    // Customized By Thirvusoft
    // Start
    ts_po_no(){
      evntBus.$emit('update_ts_po_no', this.ts_po_no);
    },
    ts_po_date(){
      evntBus.$emit('update_ts_po_date', this.ts_po_date);
    }
    // End
  },
};
</script>