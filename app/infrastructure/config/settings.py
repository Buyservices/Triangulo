from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # URL base para WebServices SOAP da Newcon
    soap_base_url: str = "https://webatendimento.consorciotriangulo.com.br"
    
    # Timeout para chamadas SOAP
    soap_timeout: int = 30
    
    # URLs específicas dos serviços
    ws_regvenda_url: str = "https://webatendimento.consorciotriangulo.com.br/wsregvenda/wsRegVenda.asmx"
    ws_atendimento_url: str = "https://webatendimento.consorciotriangulo.com.br/wsregvenda/ws_atendimento.asmx"
    ws_autorizador_url: str = "https://webatendimento.consorciotriangulo.com.br/wsregvenda/ws_autorizador.asmx"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SOAP_",
        extra="ignore",
    )
