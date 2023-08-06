
module avalon_master_interface #
  (
   //------------------------------------------------------------------------------
   // Avalon Parameter
   //------------------------------------------------------------------------------
   parameter integer C_AVM_ADDR_WIDTH = 32,
   parameter integer C_AVM_DATA_WIDTH = 32,
   parameter C_AVM_TARGET = 'h00000000
   )
  (
   //----------------------------------------------------------------------------
   // Common Clock
   //----------------------------------------------------------------------------
   input wire ACLK,
   input wire ARESETN,

   //----------------------------------------------------------------------------
   // User Bus Interface
   //----------------------------------------------------------------------------
   // Write Address
   input wire  [C_AVM_ADDR_WIDTH-1:0]   awaddr,
   input wire  [8-1:0]                  awlen,
   input wire                           awvalid,
   output wire                          awready,
  
   // Write Data
   input wire  [C_AVM_DATA_WIDTH-1:0]   wdata,
   input wire  [C_AVM_DATA_WIDTH/8-1:0] wstrb,
   input wire                           wlast,
   input wire                           wvalid,
   output wire                          wready,

   // Read Address
   input wire  [C_AVM_ADDR_WIDTH-1:0]   araddr,
   input wire  [8-1:0]                  arlen,
   input wire                           arvalid,
   output wire                          arready,

   // Read Data
   output wire [C_AVM_DATA_WIDTH-1:0]   rdata,
   output wire                          rlast,
   output wire                          rvalid,
   input wire                           rready,

   // Error
   output wire                          error,
   
   //----------------------------------------------------------------------------
   // Avalon Master Interface
   //----------------------------------------------------------------------------
   // Common
   output wire [C_AVM_ADDR_WIDTH-1:0]   avm_address,
   input  wire                          avm_waitrequest,
   output wire [C_AVM_DATA_WIDTH/8-1:0] avm_byteenable,
   output wire [8:0]                    avm_burstcount,
   
   // Read
   output wire                          avm_read,
   input  wire [C_AVM_DATA_WIDTH-1:0]   avm_readdata,
   input  wire                          avm_readdatavalid,

   // Write
   output wire                          avm_write,
   output wire [C_AVM_DATA_WIDTH-1:0]   avm_writedata
   );

  //----------------------------------------------------------------------------
  // Reset logic
  //----------------------------------------------------------------------------
  reg aresetn_r;
  reg aresetn_rr;
  reg aresetn_rrr;

  always @(posedge ACLK) begin
    aresetn_r <= ARESETN;
    aresetn_rr <= aresetn_r;
    aresetn_rrr <= aresetn_rr;
  end

  //------------------------------------------------------------------------------
  // User-logic Interface
  //------------------------------------------------------------------------------
  reg write_busy;
  reg [8:0] write_count;

  reg read_busy;
  reg [8:0] read_count;
  reg read_addr_done;
  
  reg [C_AVM_DATA_WIDTH-1:0] write_data;
  reg [C_AVM_DATA_WIDTH/8-1:0] write_strb;
  reg has_write_data;
  
  reg [C_AVM_DATA_WIDTH-1:0] write_addr;
  reg [C_AVM_ADDR_WIDTH-1:0] write_len;
  reg has_write_addr;
  
  // Write Address
  assign awready = !write_busy || (!avm_waitrequest && has_write_data);
  
  // Write Data
  assign wready = !avm_waitrequest && !has_write_data;
  
  // Read Address
  assign arready = !write_busy && !avm_waitrequest;
  
  // Read Data
  assign rdata = avm_readdata;
  assign rlast = read_count == 1;
  assign rvalid = avm_readdatavalid;

  //------------------------------------------------------------------------------
  // Avalon Interface
  //------------------------------------------------------------------------------
  // Common
  assign avm_address = awvalid? awaddr + C_AVM_TARGET : 
                       has_write_addr? write_addr + C_AVM_TARGET : 
                       araddr + C_AVM_TARGET;
  assign avm_byteenable = has_write_data? write_strb : wstrb;
  assign avm_burstcount = awvalid? awlen + 1 :
                          has_write_addr? write_len : 
                          arlen + 1;
  
  // Read
  assign avm_read = arvalid;
  
  // Write
  assign avm_write = has_write_addr? wvalid :
                     has_write_data? awvalid :
                     (awvalid || write_busy) && wvalid;
  assign avm_writedata = has_write_data? write_data : wdata;

  //------------------------------------------------------------------------------  
  always @(posedge ACLK) begin
    if (aresetn_rrr == 0) begin
      write_busy <= 0;
      write_count <= 0;
      read_busy <= 0;
      read_count <= 0;
      read_addr_done <= 0;
      write_data <= 0;
      write_strb <= 0;
      write_len <= 0;
      has_write_data <= 0;
      write_addr <= 0;
      has_write_addr <= 0;
    end else if(write_busy) begin
      if(has_write_data) begin
        if(awvalid && !avm_waitrequest) begin
          has_write_data <= 0;
          write_count <= awlen;
          if(awlen == 0) begin
            write_busy <= 0;
          end
        end
      end else if(!avm_waitrequest && wvalid) begin
        has_write_addr <= 0;
        write_count <= write_count - 1;
        if(write_count == 1) begin
          write_busy <= 0;
        end
      end
    end else if(read_busy) begin
      read_addr_done <= !avm_waitrequest;
      if(avm_readdatavalid) begin
        read_count <= read_count - 1;
        if(read_count == 1) begin
          read_busy <= 0;
        end
      end
    end else begin
      if(awvalid && wvalid) begin
        if(!avm_waitrequest) begin
          write_count <= awlen;
          if(awlen == 0) write_busy <= 0;
          else write_busy <= 1;
        end else begin
          write_count <= awlen + 1;
          write_busy <= 1;
          has_write_addr <= 1;
        end
      end else if(awvalid) begin
        write_addr <= awaddr;
        write_len <= awlen + 1;
        write_count <= awlen + 1;
        has_write_addr <= 1;
        write_busy <= 1;
      end else if(wvalid) begin
        write_data <= wdata;
        write_strb <= wstrb;
        has_write_data <= 1;
      end else if(arvalid) begin
        read_busy <= 1;
        read_count <= arlen + 1;
        read_addr_done <= !avm_waitrequest;
      end
    end
  end

  //------------------------------------------------------------------------------  
  // Error
  //------------------------------------------------------------------------------  
  assign error = 1'b0;
  
endmodule

