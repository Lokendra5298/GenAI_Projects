"""Data Loader for Sample Financial Data"""
from typing import List, Dict
from langchain.schema import Document


def get_sample_financial_data() -> List[Dict]:
    """Return sample financial metrics data"""
    return [
        {
            'ticker': 'AAPL',
            'company_name': 'Apple Inc.',
            'fiscal_year': 2023,
            'revenue': 383285000000,
            'net_income': 96995000000,
            'total_assets': 352755000000,
            'total_liabilities': 290437000000,
            'operating_cash_flow': 110543000000,
            'eps': 6.13
        },
        {
            'ticker': 'AAPL',
            'company_name': 'Apple Inc.',
            'fiscal_year': 2022,
            'revenue': 394328000000,
            'net_income': 99803000000,
            'total_assets': 352583000000,
            'total_liabilities': 302083000000,
            'operating_cash_flow': 122151000000,
            'eps': 6.15
        },
        {
            'ticker': 'MSFT',
            'company_name': 'Microsoft Corporation',
            'fiscal_year': 2023,
            'revenue': 211915000000,
            'net_income': 72361000000,
            'total_assets': 411976000000,
            'total_liabilities': 205753000000,
            'operating_cash_flow': 87582000000,
            'eps': 9.68
        },
        {
            'ticker': 'GOOGL',
            'company_name': 'Alphabet Inc.',
            'fiscal_year': 2023,
            'revenue': 307394000000,
            'net_income': 73795000000,
            'total_assets': 402392000000,
            'total_liabilities': 111158000000,
            'operating_cash_flow': 101736000000,
            'eps': 5.80
        },
    ]


def get_sample_qualitative_data() -> List[Document]:
    """Return sample qualitative financial documents"""
    return [
        Document(
            page_content="Apple's Management Discussion: The company experienced strong growth in Services revenue, driven by increased App Store sales and subscription services. iPhone sales remained stable despite market headwinds. The company continues to invest heavily in AI and machine learning capabilities.",
            metadata={'ticker': 'AAPL', 'section': 'MD&A', 'year': 2023}
        ),
        Document(
            page_content="Apple Risk Factors: Supply chain disruptions remain a significant risk, particularly related to semiconductor availability. Geopolitical tensions in Asia could impact manufacturing operations. Currency fluctuations may affect international revenue.",
            metadata={'ticker': 'AAPL', 'section': 'Risk Factors', 'year': 2023}
        ),
        Document(
            page_content="Microsoft's Management Discussion: Cloud computing revenue through Azure showed exceptional growth of 29% year-over-year. The integration of AI capabilities across product lines is driving increased customer adoption. LinkedIn and gaming divisions also contributed positively.",
            metadata={'ticker': 'MSFT', 'section': 'MD&A', 'year': 2023}
        ),
        Document(
            page_content="Microsoft Risk Factors: Cybersecurity threats pose ongoing challenges to cloud infrastructure. Regulatory scrutiny in multiple jurisdictions regarding data privacy and antitrust concerns. Competition from AWS and Google Cloud intensifying.",
            metadata={'ticker': 'MSFT', 'section': 'Risk Factors', 'year': 2023}
        ),
        Document(
            page_content="Alphabet's Management Discussion: Search advertising remains the core revenue driver, with strong performance in mobile search. YouTube ad revenue grew substantially. The company is investing significantly in AI research and development, including large language models.",
            metadata={'ticker': 'GOOGL', 'section': 'MD&A', 'year': 2023}
        ),
        Document(
            page_content="Alphabet Risk Factors: Changes in privacy regulations and cookie deprecation may impact advertising effectiveness. Increased competition in cloud computing. Regulatory investigations in EU and US regarding search dominance and app store policies.",
            metadata={'ticker': 'GOOGL', 'section': 'Risk Factors', 'year': 2023}
        ),
    ]
