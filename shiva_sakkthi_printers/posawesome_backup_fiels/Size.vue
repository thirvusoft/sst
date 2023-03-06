<template>
  <v-dialog v-model="sizeDialog" max-width="400px">
    <v-card>
      <v-card-text class="pa-0">
        <v-container>
          <v-row>
            <v-col cols="6">
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
                  ></v-text-field>
                </template>
              </v-data-table>
            </v-col>
            <v-col cols="6">
              <v-data-table
                :headers="items_headers1"
                :items="items1"
                outlined
                item-key="posa_row_id"
                class="elevation-1"
                :items-per-page="itemsPerPage"
                hide-default-footer
              >
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
     
    ],
    items_headers1: [
      { text: __('QTY'), value: 'size2', align: 'center' },
     
    ],
    items: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
    items1: [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
  }),
 
  methods: {
    submit_dialog() {
  var ts_size_text = "";
  var ts_size2_text = "";
  var total_qty=0

  for (var i = 0; i < this.items.length; i++) {
    
    if (this.items[i].size) {
      if (ts_size_text) {
        ts_size_text = ts_size_text + "," + this.items[i].size;
      } else {
        ts_size_text = ts_size_text + this.items[i].size;
      }
    }
   
  }

 
  for (var i = 0; i < this.items1.length; i++) {
    if (this.items1[i].size2) {
      if (ts_size2_text) { 
        ts_size2_text = ts_size2_text + "," + this.items1[i].size2;   
      } else {
        ts_size2_text = ts_size2_text + this.items1[i].size2;
      }
      total_qty +=parseInt(this.items1[i].size2);
    }
  }
  this.ts_size_item["ts_size"] = ts_size_text
  this.ts_size_item["ts_qty"] = ts_size2_text
  this.ts_size_item["qty"] = total_qty 

 
 
  this.ts_size_item["is_ts_size"] = "True"
  

  evntBus.$emit('ts_size_add_item', this.ts_size_item);
  
  
  this.sizeDialog = false;
  this.items = [{},{},{},{},{},{},{},{},{},{}]
  this.items1 = [{},{},{},{},{},{},{},{},{},{}] 
},
    close_dialog(){
      this.ts_size_item["is_ts_size"] = "True"
      evntBus.$emit('ts_size_add_item', this.ts_size_item);
     
    
      this.sizeDialog = false;
      this.items = [{},{},{},{},{},{},{},{},{},{}]
      this.item1 = [{},{},{},{},{},{},{},{},{},{}]
    }
  },

  created: function () {

      evntBus.$on('edit_size_for_item', (item) => {
          
          this.sizeDialog = true
          this.items = [{},{},{},{},{},{},{},{},{},{}]
          this.items1 = [{},{},{},{},{},{},{},{},{},{}]
          try{

            var ts_data = item["ts_size"].split(",")

            for (var i = 0; i<((ts_data).length); i++){
              this.items[i]={"size":ts_data[i]}
            }
          }
          catch(error){

          }
          try{

            var ts_data2 = item["ts_qty"].split(",")

            for (var i = 0; i<((ts_data2).length); i++){
              this.items1[i]={"size2":ts_data2[i]}
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