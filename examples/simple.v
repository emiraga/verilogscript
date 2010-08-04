module counter (input clk, input rst, input enable, output reg [3:0] count);
        always @ (posedge clk or posedge rst)
        begin
                if(rst)
                begin
                        count <= 0;
                end
                else
                begin:COUNT
                        while(enable)
                        begin
                                count <= count + 1;
                                disable COUNT;
                        end
                end
        end
endmodule
module dff (input clk, input d, input rst, input pre, output reg q, output q_bar);
        assign q_bar = ~q;
        always @ (posedge clk)
        begin
                if(rst)
                begin
                        q <= 0;
                end
                else if(pre)
                begin
                        q <= 1;
                end
                else
                begin
                        q <= d;
                end
        end
endmodule