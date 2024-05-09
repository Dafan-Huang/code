module sel_8_1(
    input n_EN,
    input [2:0] sel,
    input [7:0] D,
    output reg Y
    );
    
always @(n_EN or sel or D)
    if (!n_EN)
        case(sel)
            3'b000: Y = D[0];
            3'b001: Y = D[1];
            3'b010: Y = D[2];
            3'b011: Y = D[3];
            3'b100: Y = D[4];
            3'b101: Y = D[5];
            3'b110: Y = D[6];
            3'b111: Y = D[7];
            default: Y = 0; // Default case for undefined select values
        endcase
    else
        Y = 0; // When enable signal is high, output is forced to zero
endmodule


module sel_8_1_tb;

	// Inputs
	reg n_EN;
	reg [2:0] sel;
	reg [7:0] D;

	// Outputs
	wire Y;

	// Instantiate the Unit Under Test (UUT)
	sel_8_1 uut (
		.n_EN(n_EN), 
		.sel(sel), 
		.D(D), 
		.Y(Y)
	);

	initial begin
		// Initialize Inputs
		n_EN = 0;
		sel = 000;
		D = 170;

		// Wait 100 ns for global reset to finish
		#100;
		n_EN = 0;
		sel = 1;
		D = 170;
       
		#100;
		n_EN = 0;
		sel =010;
		D = 170;

 		#100;
		n_EN = 0;
		sel =011;
		D = 170;

		#100;
		n_EN = 0;
		sel =100;
		D = 170;

		#100;
		n_EN = 0;
		sel =101;
		D = 170;
	
		#100;
		n_EN = 0;
		sel =110;
		D = 170;
		
		#100;
		n_EN = 0;
		sel =111;
		D = 170;
		// Add stimulus here

	end
      
endmodule


module decoder_3_8(
    input [2:0] A,
    input EN,
    output reg [7:0] D
    );

always@(*)
begin
    case(A)
        3'b000: D = 8'b00000001;
        3'b001: D = 8'b00000010;
        3'b010: D = 8'b00000100;
        3'b011: D = 8'b00001000;
        3'b100: D = 8'b00010000;
        3'b101: D = 8'b00100000;
        3'b110: D = 8'b01000000;
        3'b111: D = 8'b10000000;
        default: D = 8'b00000000;
    endcase
end
endmodule



module deocoder_3_8_tb;

	// Inputs
	reg [2:0] A;
	reg EN;

	// Outputs
	wire [7:0] D;

	// Instantiate the Unit Under Test (UUT)
	decoder_3_8 uut (
		.A(A), 
		.EN(EN), 
		.D(D)
	);

initial begin
    // Test case 1
    A = 3'b000; EN = 1; #10;
    // Test case 2
    A = 3'b001; EN = 1; #10;
    // Test case 3
    A = 3'b010; EN = 1; #10;
    // Test case 4
    A = 3'b011; EN = 1; #10;
    // Test case 5
    A = 3'b100; EN = 1; #10;
    // Test case 6
    A = 3'b101; EN = 1; #10;
    // Test case 7
    A = 3'b110; EN = 1; #10;
    // Test case 8
    A = 3'b111; EN = 1; #10;
    // Disable decoder
    EN = 0; #10;
    // End simulation
    $finish;
end
      
endmodule


module c_74LS161(
    input CP,
    input CR,
    input LD,
    input EP,
    input ET,
    input [3:0] D,
    output reg [3:0] Q,
    output reg CO
);

always @(posedge CP or negedge CR) begin
    if(~CR) begin 
        Q <= 4'b0000;
        CO <= 1'b0;
    end
    else if(~LD) begin 
        Q <= D;
        CO <= 1'b0;
    end
    else begin 
        case({EP, ET})
            2'bx0: begin Q <= Q; CO <= 1'b0; end
            2'b01: begin Q <= Q; CO <= CO; end
            2'b11: begin 
                Q <= Q + 1'b1; 
                CO <= (Q == 4'b1111); 
            end
        endcase
    end
end

endmodule



module c_74LS161_tb;

	// Inputs
	reg CP;
	reg CR;
	reg LD;
	reg EP;
	reg ET;
	reg [3:0] D;

	// Outputs
	wire [3:0] Q;
	wire CO;

	// Instantiate the Unit Under Test (UUT)
	c_74LS161 uut (
		.CP(CP), 
		.CR(CR), 
		.LD(LD), 
		.EP(EP), 
		.ET(ET), 
		.D(D), 
		.Q(Q), 
		.CO(CO)
	);

	initial 
		CP = 1;
	always
		#5 CP = ~CP;

	initial begin
		
		//同步并入
		CR = 1;
		LD = 0;
		D = 4'b1010;
		//EP = x;ET = x;
		#100;
		
		//异步清零
		CR = 0;
		EP = 0;
		ET = 0;
		D = 4'b0000;
		#100;
		
		//计数
		CR = 1;
		LD = 1;
		EP = 1;ET = 1;
		#150;
		
		//保持CO=Q3Q2Q1Q0
		CR = 1;
		LD = 1;
		EP = 0;
		ET = 1;
		#100;
		
		//保持CO=0
		CR = 1;
		LD = 1;
		//EP = x;
		ET = 1;
		#100;
		
						
	end
      
endmodule

