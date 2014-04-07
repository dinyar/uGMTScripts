-- Top-level design for MP7 base firmware
--
-- Dave Newbold, July 2012

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

use work.ipbus.all;
use work.ipbus_trans_decl.all;
use work.mp7_data_types.all;
use work.mp7_readout_decl.all;

entity top is
	generic(
		LHC_BUNCH_COUNT: integer := 3564;
		NQUAD: natural := 1; -- 12;
		CLOCK_RATIO: integer := 4;
		NREFCLK: integer := 6
	);
	port(
		eth_clkp, eth_clkn: in std_logic;
		eth_txp, eth_txn: out std_logic;
		eth_rxp, eth_rxn: in std_logic;
		leds: out std_logic_vector(11 downto 0);
		ebi_nwe: in std_logic;
		ebi_nrd: in std_logic;
		ebi_d: inout std_logic_vector(15 downto 0);
		ebi_a: inout std_logic_vector(16 downto 1);
		clk40_in_p: in std_logic;
		clk40_in_n: in std_logic;
		ttc_in_p: in std_logic;
		ttc_in_n: in std_logic;
		clk_cntrl: out std_logic_vector(17 downto 0);
		si5326_rst: out std_logic;
		si5326_int: in std_logic;
		si5326_lol: in std_logic;
		si5326_scl: out std_logic;
		si5326_sda: inout std_logic;
		minipod_top_rst_b: out std_logic;
		minipod_top_scl: out std_logic;
		minipod_top_sda_o: out std_logic;
		minipod_top_sda_i: in std_logic;
		minipod_bot_rst_b: out std_logic;
		minipod_bot_scl: out std_logic;
		minipod_bot_sda_o: out std_logic;
		minipod_bot_sda_i: in std_logic;
		mezz_p: out std_logic_vector(29 downto 0);
		mezz_n: out std_logic_vector(29 downto 0);
		refclkp: in std_logic_vector(NREFCLK - 1 downto 0);
		refclkn: in std_logic_vector(NREFCLK - 1 downto 0);
		rxp: in std_logic_vector(4 * NQUAD - 1 downto 0);
		rxn: in std_logic_vector(4 * NQUAD - 1 downto 0);
		txp: out std_logic_vector(4 * NQUAD - 1 downto 0);
		txn: out std_logic_vector(4 * NQUAD - 1 downto 0) 
	);

end top;

architecture rtl of top is
	
	signal clk_ipb, rst_ipb, clk160, rst160, clk240, rst240, clk40, rst40: std_logic;
	signal clk40_rst, clk40_sel, clk40_lock, clk40_stop, nuke, soft_rst: std_logic;
	signal clk_p, rst_p: std_logic;
	
	signal si5326_sda_o: std_logic;
	
	signal ipb_in_ctrl, ipb_in_ttc, ipb_in_datapath, ipb_in_readout, ipb_in_payload: ipb_wbus;
	signal ipb_out_ctrl, ipb_out_ttc, ipb_out_datapath, ipb_out_readout, ipb_out_payload: ipb_rbus;
	
	signal payload_d, payload_q: ldata(NQUAD * 4	- 1 downto 0);
	signal qsel: std_logic_vector(7 downto 0);
	signal ttc_l1a, dist_lock: std_logic;
	signal ttc_cmd, ttc_cmd_dist: std_logic_vector(3 downto 0);
	signal bunch_ctr: std_logic_vector(11 downto 0);
	signal evt_ctr, orb_ctr: std_logic_vector(23 downto 0);

	signal clkmon: std_logic_vector(2 downto 0);

	signal cap_bus: daq_cap_bus;
	signal daq_bus_top, daq_bus_bot: daq_bus;
	
begin

-- Clocks and control IO

	infra: entity work.mp7_infra
		generic map(
			MAC_ADDR => X"000a3501eaf1",
			IP_ADDR => X"c0a80080"
		)
		port map(
			gt_clkp => eth_clkp,
			gt_clkn => eth_clkn,
			gt_txp => eth_txp,
			gt_txn => eth_txn,
			gt_rxp => eth_rxp,
			gt_rxn => eth_rxn,
			leds => leds,
			uc_pipe_nrd => ebi_nrd, 
			uc_pipe_nwe => ebi_nwe, 
			uc_pipe => ebi_d, 
			uc_spi_miso => ebi_a(7), 
			uc_spi_mosi => ebi_a(6), 
			uc_spi_sck => ebi_a(5), 
			uc_spi_cs_b => ebi_a(4), 
			clk_ipb => clk_ipb,
			rst_ipb => rst_ipb,
			clk40ish => clk40ish,
			nuke => nuke,
			soft_rst => soft_rst,
			ipb_in_ctrl => ipb_out_ctrl,
			ipb_out_ctrl => ipb_in_ctrl,
			ipb_in_ttc => ipb_out_ttc,
			ipb_out_ttc => ipb_in_ttc,
			ipb_in_datapath => ipb_out_datapath,
			ipb_out_datapath => ipb_in_datapath,
			ipb_in_readout => ipb_out_readout,
			ipb_out_readout => ipb_in_readout,
			ipb_in_payload => ipb_out_payload,
			ipb_out_payload => ipb_in_payload
		);

-- Control registers and board IO
		
	ctrl: entity work.mp7_ctrl
		generic map(
			LHC_BUNCH_COUNT => LHC_BUNCH_COUNT,
			NQUAD => NQUAD,
			CLOCK_RATIO => CLOCK_RATIO
		)
		port map(
			clk => clk_ipb,
			rst => rst_ipb,
			ipb_in => ipb_in_ctrl,
			ipb_out => ipb_out_ctrl,
			nuke => nuke,
			soft_rst => soft_rst,
			qsel => qsel,
			clk40_rst => clk40_rst,
			clk40_sel => clk40_sel,
			clk40_lock => clk40_lock,
			clk40_stop => clk40_stop,
			clk_cntrl => clk_cntrl,
			si5326_rst => si5326_rst,
			si5326_int => si5326_int,
			si5326_lol => si5326_lol,
			si5326_scl => si5326_scl,
			si5326_sda_i => si5326_sda,
			si5326_sda_o => si5326_sda_o,
			minipod_top_rst_b => minipod_top_rst_b,
			minipod_top_scl => minipod_top_scl,
			minipod_top_sda_o => minipod_top_sda_o,
			minipod_top_sda_i => minipod_top_sda_i,
			minipod_bot_rst_b => minipod_bot_rst_b,
			minipod_bot_scl => minipod_bot_scl,
			minipod_bot_sda_o => minipod_bot_sda_o,
			minipod_bot_sda_i => minipod_bot_sda_i
		);
		
	si5326_sda <= '0' when si5326_sda_o = '0' else 'Z';

-- TTC signal handling
	
	ttc: entity work.mp7_ttc
		generic map(
			LHC_BUNCH_COUNT => LHC_BUNCH_COUNT
		)
		port map(
			clk => clk_ipb,
			rst => rst_ipb,
			mmcm_rst => clk40_rst,
			sel => clk40_sel,
			lock => clk40_lock,
			stop => clk40_stop,
			ipb_in => ipb_in_ttc,
			ipb_out => ipb_out_ttc,
			clk40_in_p => clk40_in_p,
			clk40_in_n => clk40_in_n,
			clk40ish_in => clk40ish,
			clk40 => clk40,
			rsto40 => rst40,
			clk160 => clk160,
			rsto160 => rst160,
			clk240 => clk240,
			rsto240 => rst240,
			ttc_in_p => ttc_in_p,
			ttc_in_n => ttc_in_n,
			ttc_cmd => ttc_cmd,
			ttc_cmd_dist => ttc_cmd_dist,
			ttc_l1a => ttc_l1a,
			dist_lock => dist_lock,
			bunch_ctr => bunch_ctr,
			evt_ctr => evt_ctr,
			orb_ctr => orb_ctr,			
			monclk => clkmon
		);
		
		clk_p <= clk240 when CLOCK_RATIO = 6 else clk160;
		rst_p <= rst240 when CLOCK_RATIO = 6 else rst160;
		
-- MGTs, buffers and TTC fanout
		
	datapath: entity work.mp7_datapath
		generic map(
			NQUAD => NQUAD,
			CLOCK_RATIO => CLOCK_RATIO,
			LHC_BUNCH_COUNT => LHC_BUNCH_COUNT,
			NREFCLK => NREFCLK
		)
		port map(
			clk => clk_ipb,
			rst => rst_ipb,
			ipb_in => ipb_in_datapath,
			ipb_out => ipb_out_datapath,
			qsel => qsel,
			clk_p => clk_p,
			rst_p => rst_p,
			ttc_cmd => ttc_cmd_dist,
			lock => dist_lock,
			cap_bus => cap_bus,
			daq_bus_in => daq_bus_top,
			daq_bus_out => daq_bus_bot,
			refclkp => refclkp,
			refclkn => refclkn,
			rxp => rxp,
			rxn => rxn,
			txp => txp,
			txn => txn,
			clkmon => clkmon,
			payload_d => payload_d,
			payload_q => payload_q
		);

-- Readout
		
	readout: entity work.mp7_readout
		generic map(
			CLOCK_RATIO => CLOCK_RATIO
		)
		port map(
			clk => clk_ipb,
			rst => rst_ipb,
			ipb_in => ipb_in_readout,
			ipb_out => ipb_out_readout,
			clk40 => clk40,
			rst40 => rst40,
			ttc_cmd => ttc_cmd,
			l1a => ttc_l1a,
			bunch_ctr => bunch_ctr,
			evt_ctr => evt_ctr,
			orb_ctr => orb_ctr,
			clk_p => clk_p,
			rst_p => rst_p,
			cap_bus => cap_bus,
			daq_bus_out => daq_bus_top,
			daq_bus_in => daq_bus_bot
		);
		
-- Payload
		
	payload: entity work.mp7_payload
		generic map(
			NCHAN => 4 * NQUAD,
			PIPELINE_STAGES => CLOCK_RATIO
		)
		port map(
			clk => clk_ipb,
			rst => rst_ipb,
			ipb_in => ipb_in_payload,
			ipb_out => ipb_out_payload,			
			clk_p => clk_p,
			d => payload_d,
			q => payload_q
		);

-- Debugging connector
		
	mezz_inst: entity work.mezz_out_lvds
		generic map(
			NMEZZ => mezz_p'length
		)
		port map(
			mezz => (others => '0'),
			mezz_en => (others => '0'),
			mezz_n => mezz_n,
			mezz_p => mezz_p
		);
		
end rtl;

