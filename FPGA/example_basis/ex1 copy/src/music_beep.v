module music_beep (

  input   wire              clk,
  input   wire              rst_n,
  
  output  wire              beep
);

  wire          [5:0]       cnt;
  wire          [4:0]       music;
  wire          [31:0]      divnum;
  
  speed_ctrl speed_ctrl_inst(

      .clk                  (clk),
      .rst_n                (rst_n),
      
      .cnt                  (cnt)
    );
    
  music_mem music_mem_inst(

      .clk                  (clk),
      .rst_n                (rst_n),
      
      .cnt                  (cnt),
      
      .music                (music)
    );
    
  cal_divnum cal_divnum_inst(
  
      .clk                  (clk),
      .rst_n                (rst_n),
      
      .music                (music),
      
      .divnum               (divnum)
    );

  wave_gen wave_gen_inst(

      .clk                  (clk),
      .rst_n                (rst_n),
      
      .divnum               (divnum),
      
      .beep                 (beep)
    );
    
endmodule