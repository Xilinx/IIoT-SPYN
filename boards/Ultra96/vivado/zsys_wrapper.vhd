--Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
----------------------------------------------------------------------------------
--Tool Version: Vivado v.2018.2_AR71601 (win64) Build 2258646 Thu Jun 14 20:03:12 MDT 2018
--Date        : Wed Jan 30 20:46:45 2019
--Host        : XOWJOHNMCD31 running 64-bit major release  (build 9200)
--Command     : generate_target zsys_wrapper.bd
--Design      : zsys_wrapper
--Purpose     : IP block netlist
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VCOMPONENTS.ALL;
entity zsys_wrapper is
  port (
    BT_ctsn : in STD_LOGIC;
    BT_rtsn : out STD_LOGIC;
    ENC_A : in STD_LOGIC;
    ENC_B : in STD_LOGIC;
    ENC_I : in STD_LOGIC;
    GH : out STD_LOGIC_VECTOR ( 2 downto 0 );
    GL : out STD_LOGIC_VECTOR ( 2 downto 0 );
    SCLK : out STD_LOGIC;
    SDI1 : in STD_LOGIC;
    SDI2 : in STD_LOGIC;
    SDI3 : in STD_LOGIC;
    SDV : in STD_LOGIC
  );
end zsys_wrapper;

architecture STRUCTURE of zsys_wrapper is
  component zsys is
  port (
    ENC_A : in STD_LOGIC;
    ENC_B : in STD_LOGIC;
    ENC_I : in STD_LOGIC;
    SDI1 : in STD_LOGIC;
    SDI2 : in STD_LOGIC;
    SDI3 : in STD_LOGIC;
    SDV : in STD_LOGIC;
    SCLK : out STD_LOGIC;
    GH : out STD_LOGIC_VECTOR ( 2 downto 0 );
    GL : out STD_LOGIC_VECTOR ( 2 downto 0 );
    BT_ctsn : in STD_LOGIC;
    BT_rtsn : out STD_LOGIC
  );
  end component zsys;
begin
zsys_i: component zsys
     port map (
      BT_ctsn => BT_ctsn,
      BT_rtsn => BT_rtsn,
      ENC_A => ENC_A,
      ENC_B => ENC_B,
      ENC_I => ENC_I,
      GH(2 downto 0) => GH(2 downto 0),
      GL(2 downto 0) => GL(2 downto 0),
      SCLK => SCLK,
      SDI1 => SDI1,
      SDI2 => SDI2,
      SDI3 => SDI3,
      SDV => SDV
    );
end STRUCTURE;
