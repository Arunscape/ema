import pandas as pd
import yfinance as yf
from pytickersymbols import PyTickerSymbols
import warnings

warnings.filterwarnings(
    "ignore",
    message="The 'unit' keyword in TimedeltaIndex construction is deprecated and will be removed in a future version. Use pd.to_timedelta instead.",
    category=FutureWarning,
    module="yfinance.utils",
)

yf.set_tz_cache_location("./.yfinance_cache")


def ema_crosses_ma(ticker):
    # Download historical stock data
    data = yf.download(ticker, start="2022-01-01", end="2022-12-31")

    # Calculate 20-day EMA and 50-day MA
    data["EMA_20"] = data["Close"].ewm(span=20, adjust=False).mean()
    data["MA_50"] = data["Close"].rolling(window=50).mean()

    # Find rows where EMA crosses MA (upward)
    crosses_up = data[
        (data["EMA_20"] > data["MA_50"])
        & (data["EMA_20"].shift(1) < data["MA_50"].shift(1))
    ]

    # Find rows where EMA crosses MA (downward)
    crosses_down = data[
        (data["EMA_20"] < data["MA_50"])
        & (data["EMA_20"].shift(1) > data["MA_50"].shift(1))
    ]

    # Print results
    print("Dates where 20EMA crosses above 50MA (upward):")
    print(crosses_up[["Close", "EMA_20", "MA_50"]])
    print("\nDates where 20EMA crosses below 50MA (downward):")
    print(crosses_down[["Close", "EMA_20", "MA_50"]])


# Example usage
# ticker_symbol = "AAPL"  # Change this to the desired stock symbol
# ema_crosses_ma(ticker_symbol)

# basically get a list of all the tickers you want.
# it can be formatted like this:
# tickers = ["AAPL", "NVDA", "AMD", "PLTR", "INTC"]
tickers = PyTickerSymbols()
dow_jones = tickers.get_dow_jones_nyc_yahoo_tickers()
for ticker in dow_jones:
    print(f"\nTicker: {ticker}")
    ema_crosses_ma(ticker)


tsx = [
    "RY",
    "SHOP",
    "TD",
    "CNR",
    "CP",
    "ENB",
    "TRI",
    "BN",
    "BMO",
    "CNQ",
    "CSU",
    "ATD",
    "BNS",
    "CM",
    "SU",
    "MFC",
    "WCN",
    "TRP",
    "NGT",
    "BCE",
    "QSR",
    "IMO",
    "SLF",
    "L",
    "CVE",
    "GWO",
    "IFC",
    "GIB.A",
    "FFH",
    "QSP.UN",
    "NA",
    "ABX",
    "T",
    "RCI.B",
    "NTR",
    "RCI.A",
    "AEM",
    "DOL",
    "FNV",
    "WPM",
    "TECK.B",
    "TECK.A",
    "CCO",
    "FTS",
    "POW",
    "WSP",
    "PPL",
    "H",
    "WN",
    "BEP.UN",
    "BAM",
    "MG",
    "BIP.UN",
    "TOU",
    "TPX.B",
    "GFL",
    "IVN",
    "RBA",
    "TFII",
    "MRU",
    "OTEX",
    "OVV",
    "CDAY",
    "EMA",
    "ARX",
    "STN",
    "SAP",
    "DSG",
    "CCL.A",
    "FSV",
    "CCL.B",
    "CHP.UN",
    "TIH",
    "X",
    "IAG",
    "CAE",
    "K",
    "IGM",
    "EFN",
    "LUN",
    "PHYS",
    "EMP.A",
    "WFG",
    "FM",
    "CAR.UN",
    "CTC.A",
    "ONEX",
    "GIL",
    "PKI",
    "ATRL",
    "CTC",
    "U.UN",
    "ALA",
    "QBR.A",
    "QBR.B",
    "KEY",
    "CIGI",
    "DOO",
    "BLCO",
    "MEG",
    "AC",
    "BYD",
    "BIPC",
    "AGI",
    "PAAS",
    "CU",
    "CLS",
    "BNRE",
    "BEPC",
    "NPI",
    "FTT",
    "REI.UN",
    "EDV",
    "CEF",
    "AQN",
    "NXE",
    "CPG",
    "PSK",
    "WCP",
    "PSLV",
    "NVEI",
    "BBD.B",
    "BBD.A",
    "GRT.UN",
    "BTO",
    "KXS",
    "SJ",
    "CS",
    "ATZ",
    "DFY",
    "ATS",
    "CPX",
    "MX",
    "SRU.UN",
    "ACO.X",
    "ACO.Y",
    "PBH",
    "TCN",
    "BHC",
    "LNR",
    "ERF",
    "BEI.UN",
    "DIR.UN",
    "POU",
    "TIXT",
    "LUG",
    "CIA",
    "OR",
    "TOY",
    "BTE",
    "FCR.UN",
    "ELF",
    "TFPM",
    "EQB",
    "CRT.UN",
    "GLXY",
    "GEI",
    "BBUC",
    "ELD",
    "BLX",
    "MFI",
    "PRMW",
    "SES",
    "LSPD",
    "IGAF",
    "TA",
    "ZCPB",
    "CCA",
    "CWB",
    "RUS",
    "TPZ",
    "WPK",
    "GSY",
    "SSRM",
    "ATH",
    "FIL",
    "CIX",
    "RCH",
    "HBM",
    "FN",
    "SPB",
    "VET",
    "PXT",
    "BB",
    "EIF",
    "NVA",
    "STLC",
    "CGG",
    "CJT",
    "AIF",
    "FRU",
    "ENGH",
    "SVI",
    "LIF",
    "IPCO",
    "NWC",
    "TLRY",
    "OGC",
    "TSU",
    "EQX",
    "CEE",
    "FR",
    "WTE",
    "BDGI",
    "GOOS",
    "MEQ",
    "AAV",
    "KNT",
    "MDA",
    "EFR",
    "DPM",
    "OLA",
    "HWX",
    "CG",
    "CAS",
    "NFI",
    "LNF",
    "MTL",
    "IE",
    "GCG",
    "AYA",
    "PD",
    "MRC",
    "TXG",
    "SIS",
    "LB",
    "SEA",
    "ET",
    "MRE",
    "ASTL",
    "SIL",
    "AFN",
    "FOM",
    "AOI",
    "KEL",
    "CEU",
    "IFP",
    "CJ",
    "BITF",
    "WELL",
    "PBL",
    "OSK",
    "LAC",
    "HUT",
    "ARE",
    "EFX",
    "NOA",
    "BDT",
    "CF",
    "FCU",
    "NBLY",
    "ALS",
    "CMG",
    "FSZ",
    "SEC",
    "CGI",
    "ECN",
    "KRR",
    "OBE",
    "WJX",
    "URE",
    "FEC",
    "SGY",
    "CR",
    "HRX",
    "TF",
    "GUD",
    "RSI",
    "ALC",
    "PRL",
    "EXE",
    "IAU",
    "CGO",
    "MKP",
    "SVM",
    "ARIS",
    "BDI",
    "SLS",
    "LEV",
    "WEED",
    "SDE",
    "DTOL",
    "SKE",
    "ACQ",
    "AGF.B",
    "REAL",
    "CHR",
    "GBT",
    "PNE",
    "MAL",
    "CFW",
    "ISV",
    "DIV",
    "TWC",
    "VGCX",
    "HLF",
    "FC",
    "DXT",
    "TWM",
    "ECOR",
    "III",
    "KBL",
    "GRA",
    "SOLG",
    "VLE",
    "PAY",
    "GGD",
    "ECO",
    "AR",
    "AIM",
    "ADN",
    "GAU",
    "QIPT",
    "ACB",
    "ETG",
    "QFOR",
    "ENS",
    "CKI",
    "PPTA",
    "DR",
    "BK",
    "MXG",
    "AMC",
    "GH",
    "ARG",
    "GOLD",
    "QTRH",
    "IPO",
    "ADW.A",
    "NANO",
    "MSA",
    "CJR.B",
    "FSY",
    "Y",
    "LUC",
    "EDT",
    "BNE",
    "TRZ",
    "GXE",
    "BRAG",
    "SMT",
    "DCM",
    "LGO",
    "CXI",
    "HMM.A",
    "GDV",
    "MND",
    "AII",
    "HAI",
    "XTRA",
    "STC",
    "GDC",
    "PTM",
    "NB",
    "WPRT",
    "FTG",
    "NEXT",
    "VLN",
    "SHLE",
    "SXP",
    "XAU",
    "TTNM",
    "PSD",
    "FORA",
    "SPLT",
    "CRRX",
    "COG",
    "RS",
    "GEO",
    "ASM",
    "GURU",
    "STGO",
    "MDP",
    "MCB",
    "AKT.A",
    "ICE",
    "TVA.B",
    "BUI",
    "MPVD",
    "GENM",
    "MBX",
    "ME",
    "ATE",
    "XTG",
    "EAGR",
    "ACD",
    "APS",
    "NHK",
    "MDNA",
    "ATCU",
    "AVCN",
    "MIN",
    "CCM",
    "OPT",
    "NUMI",
    "EGLX",
    "PMT",
    "BU",
    "TSK",
    "BOND",
    "RTG",
    "UNI",
    "CWL",
    "BSX",
    "FOOD",
    "ANRG",
    "DBO",
    "FT",
    "FANS",
    "BKI",
    "FDGE",
    "ADCO",
    "BRY",
    "ASND",
    "AUMN",
    "ELEF",
    "SVB",
    "AXIS",
    "VQS",
    "DN",
    "EXN",
    "AAB",
    "APLI",
]

for ticker in tsx:
    print(f"\nTicker: {ticker}")
    ema_crosses_ma(ticker)
    
