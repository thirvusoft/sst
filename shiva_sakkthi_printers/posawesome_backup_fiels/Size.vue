<template>
  <v-dialog v-model="sizeDialog" max-width="500px">
    <v-card>
      <v-card-text class="pa-0">
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-data-table
                :headers="items_headers"
                :items="items"
                outlined
                item-key="posa_row_id"
                class="elevation-1"
                :items-per-page="itemsPerPage"
                hide-default-footer
              >
                <template v-slot:item.size="{ item }">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    background-color="white"
                    hide-details
                    v-model="item.size"
                    @input="get_avl_qty(item, $event)"
                  ></v-text-field>
                </template>
                <template v-slot:item.avl_qty="{ item }">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    background-color="white"
                    hide-details
                    v-model="item.avl_qty"
                  ></v-text-field>
                </template>
                <template v-slot:item.size2="{ item }">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    background-color="white"
                    hide-details
                    v-model="item.size2"
                  ></v-text-field>
                </template>
                <template v-slot:item.stock_qty="{ item }">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    background-color="white"
                    hide-details
                    v-model="item.stock_qty"
                  ></v-text-field>
                </template>
              </v-data-table>
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
</template>

<script>
import { evntBus } from '../../bus';
export default {
  data: () => ({
    sizeDialog: false,
    itemsPerPage: 10,

    items_headers: [
      { text: __('Size'), value: 'size', align: 'center' },
      { text: __('Ordered QTY'), value: 'size2', align: 'center' },
      { text: __('Available QTY'), value: 'avl_qty', align: 'center' },
      { text: __('Stock Qty'), value: 'stock_qty', align: 'center' },

    ],

    items: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
  }),
 
  methods: {
    get_avl_qty(item){

      if (item.size){
        const vm = item

        const args = {
          ts_customer : this.ts_size_item["customer"],
          ts_size : item.size,
          item_code: this.ts_size_item["item_code"]
        };

        frappe.call({
          method: 'posawesome.posawesome.api.posapp.get_actual_qty',
          args: args,
          async: false,

          callback: function (r) {
            vm.avl_qty = r.message;
          }

        })
      }
      else{
        item.avl_qty = "";
      }
    },

    submit_dialog() {
      var ts_size_text = "";
      var ts_size2_text = "";
      var ts_avl_qty_text = "";
      var ts_stock_qty = "";
      var total_qty = 0;
      var ts_check = true;

      for (var i = 0; i < this.items.length; i++) {
        // if (this.items[i].avl_qty == "0" && !this.ts_size_item["ts_profile_stock"]){
          // evntBus.$emit('show_mesage', {
          //   text: `Stock Entry Not Found For Size ${this.items[i].size}`,
          //   color: 'error',
          // });
          // ts_check = false;
          // return;
        // }
        // else{
          if (this.items[i].stock_qty){
            var ts_stock_qtys = this.items[i].stock_qty
          }
          else{
            var ts_stock_qtys = 0
          }
          
          if (this.items[i].size2 <= (parseInt(this.items[i].avl_qty) + parseInt(ts_stock_qtys))){
            if (this.items[i].size) {
              if (i == 0){
                var ts_check_size = "true"
              }
              if (ts_size_text) {
                ts_size_text = ts_size_text + "," + this.items[i].size;
              } else {
                ts_size_text = ts_size_text + this.items[i].size;
                
              }
              
            }
            else{
              if (i == 0){
                var ts_check_size = "false"
              }
            }

            if (this.items[i].size2) {
              if (i == 0){
                var ts_check_size1 = "true"
              }
              if (ts_size2_text) { 
                ts_size2_text = ts_size2_text + "," + this.items[i].size2;   
              } else {
                ts_size2_text = ts_size2_text + this.items[i].size2;
              }

              if (ts_avl_qty_text) { 
                ts_avl_qty_text = ts_avl_qty_text + "," + this.items[i].avl_qty;   
              } else {
                ts_avl_qty_text = ts_avl_qty_text + this.items[i].avl_qty;
              }
              
              total_qty += parseInt(this.items[i].size2);
            }
            else{
              if (i == 0){
                var ts_check_size1 = "false"
              }
            }

            if (ts_stock_qty) { 
              ts_stock_qty = ts_stock_qty + "," +  ts_stock_qtys;   
            } else {
              ts_stock_qty = ts_stock_qty + ts_stock_qtys;
            }
          }
          else{
            if (this.items[i].size && !this.ts_size_item["ts_profile_stock"]) {
              evntBus.$emit('show_mesage', {
                text: `QTY Should Not Be Greater Than Available Qty For Size ${this.items[i].size}`,
                color: 'error',
              });
              ts_check = false;
              return;
            }
          }
        // }
      }
      
      var ts_size_len = ts_size_text.split(",")
      var ts_size2_len = ts_size2_text.split(",")

      if (ts_size_len.length == ts_size2_len.length && ts_check_size1 == ts_check_size && ts_check){
        
        this.ts_size_item["ts_size"] = ts_size_text
        this.ts_size_item["ts_qty"] = ts_size2_text
        this.ts_size_item["avl_qty"] = ts_avl_qty_text
        this.ts_size_item["qty"] = total_qty 
        this.ts_size_item["ts_stock_qty"] = ts_stock_qty

        this.ts_size_item["is_ts_size"] = "True"
      
        evntBus.$emit('ts_size_add_item', this.ts_size_item);
        
        this.sizeDialog = false;
        this.items = [{},{},{},{},{},{},{},{},{},{}]
      }
      else{
        if (ts_check){
          evntBus.$emit('show_mesage', {
              text: `Please Check The Size and Qty`,
              color: 'error',
          });
          return;
        }
      }
    },

    close_dialog(){
      this.ts_size_item["is_ts_size"] = "True"
      evntBus.$emit('ts_size_add_item', this.ts_size_item);
     
      this.sizeDialog = false;
      this.items = [{},{},{},{},{},{},{},{},{},{}]
    }
  },

  created: function () {

      evntBus.$on('edit_size_for_item', (item) => {
          
          this.sizeDialog = true

          this.items = [{},{},{},{},{},{},{},{},{},{}]
          
          try{

            var ts_data = item["ts_size"].split(",")
            var ts_data2 = item["ts_qty"].split(",")
            var ts_data3 = item["avl_qty"].split(",")
            var ts_data4 = item["ts_stock_qty"].split(",")

            for (var i = 0; i<((ts_data).length); i++){
              this.items[i] = {"size":ts_data[i], "size2":ts_data2[i], "avl_qty": ts_data3[i], "stock_qty":ts_data4[i]}
            }
          }
          catch(error){

          }

          this.ts_size_item = item
          this.ts_size_item["is_ts_size_edit"] = "True"
      });
    },
};
  </script>