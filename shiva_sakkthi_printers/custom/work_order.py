def change_warehouse(self,action):
    if(self.fg_warehouse!='Ready To Packing - SST'):
        self.fg_warehouse='Ready To Packing - SST'
    
def submit_wo(self, event):
    self.flags.ignore_mandatory=True
    self.flags.ignore_permissions=True
    self.submit()