<template>
  <v-dialog v-model="sizeDialog" max-width="600px">
    <v-card>
      <v-card-text class="pa-0">
        <v-data-table
          :headers="items_headers"
          :items="items"
          item-key="posa_row_id"
          class="elevation-1"
          :items-per-page="itemsPerPage"
          hide-default-footer
        >
    
        <template v-slot:item.size="{ item }">
          <v-text-field
            dense
            color="primary"
            background-color="white"
            hide-details
            v-model="item.size"
          ></v-text-field>
        </template>
        
        </v-data-table>
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
      itemsPerPage:10,
      items_headers: [
        { text: __('Size'), value: 'size', align: 'center' }
      ],
      items:[{},{},{}],
  }),
  methods: {
    submit_dialog(){
      var ts_size_text = ""

      for (var i = 0; i<((this.items).length); i++){
        if (this.items[i].size){
         
          if (ts_size_text){
            ts_size_text = ts_size_text + ", " + this.items[i].size
          }

          else{
            ts_size_text = ts_size_text+this.items[i].size
          }
            
        }
      }
      this.ts_size_item["ts_size"] = ts_size_text
      this.ts_size_item["is_ts_size"] = "True"

      evntBus.$emit('ts_size_add_item', this.ts_size_item);

      this.sizeDialog = false;
      this.items = [{},{},{}]

    },
    close_dialog(){
      this.ts_size_item["is_ts_size"] = "True"
      evntBus.$emit('ts_size_add_item', this.ts_size_item);
    
      this.sizeDialog = false;
      this.items = [{},{},{}]
    }
  },

  created: function () {

      evntBus.$on('edit_size_for_item', (item) => {
          
          this.sizeDialog = true
          this.items = [{},{},{}]
          try{

            var ts_data = item["ts_size"].split(",")

            for (var i = 0; i<((ts_data).length); i++){
              this.items[i]={"size":ts_data[i]}
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