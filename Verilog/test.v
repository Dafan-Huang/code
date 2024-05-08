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
