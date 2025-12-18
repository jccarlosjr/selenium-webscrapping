from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from subprocess import CREATE_NO_WINDOW 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from scrapper.config import LOCAL_USER_PATH
from time import sleep
import json


def alert_confirm(driver):
    try:
        wait = WebDriverWait(driver, 1)
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except:
        pass


def find_xpath(driver: webdriver.Chrome, xpath: str):
    """
    Depois de uma espera implícita, busca o elemento baseado no XPATH
    :param driver: A instância do webdriver em execução.
    :param xpath: string para o xpath do elemento.
    :return: O elemento encontrado
    """
    wait = WebDriverWait(driver, 3)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element = driver.find_element(By.XPATH, xpath)
    return element


def find_all_css(driver: webdriver.Chrome, selector: str):
    """
    Aguarda e retorna TODOS os elementos encontrados pelo CSS selector
    """
    wait = WebDriverWait(driver, 10)
    elements = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
    return elements


def clean_sendkeys(element, keys):
    """
    Seleciona e apaga qualquer valor dentro de um input, adicionando um novo texto no final
    :param element: O elemento do input.
    :param keys: string para o texto final do elemento.
    :return: O elemento encontrado
    """
    element.send_keys(Keys.SHIFT, Keys.END + Keys.BACK_SPACE)
    element.send_keys(Keys.SHIFT, Keys.HOME + Keys.BACK_SPACE)
    sleep(1)
    element.send_keys(keys)
    element.send_keys(Keys.TAB)


def login(driver):
    driver.get('https://gestao.sistemacorban.com.br/index.php/auth/login')
    find_xpath(driver, '//*[@id="exten"]').send_keys("gerente@26111")
    find_xpath(driver, '//*[@id="password"]').send_keys("Van1234@")
    find_xpath(driver, '//*[@id="button-sigin"]').click()
    alert_confirm(driver)


def search_by_cpf(driver, cpf):
    find_xpath(driver, '//*[@id="typeOfDataSent"]').click()
    find_xpath(driver, '//*[@id="typeOfDataSent"]/option[1]').click()
    cpf_input = find_xpath(driver, '//*[@id="dataToReceptivo"]')
    cpf_input.send_keys(str(cpf).strip().replace(".", "").replace("-", ""), Keys.ENTER)

    nb_list = []
    response_list = []

    card_beneficios = find_all_css(driver, 'button.card--selecionar-beneficio')

    for btn in card_beneficios:
        onclick = btn.get_attribute("onclick")
        numero = onclick.replace("consultarBeneficio(", "").replace(")", "")
        nb_list.append(numero)

    for nb in nb_list:
        response = search_nb_data(driver, nb)
        response_list.append(response)

    return response_list


def search_nb_data(driver, nb):
    find_xpath(driver, '//*[@id="typeOfDataSent"]').click()
    find_xpath(driver, '//*[@id="typeOfDataSent"]/option[2]').click()
    nb_input = find_xpath(driver, '//*[@id="dataToReceptivo"]')
    nb_input.send_keys(nb, Keys.ENTER)
    find_xpath(driver, '//*[@id="btnOcultar"]').click()
    dados = {}

    dados["nb_uf"] = find_xpath(driver, '//*[@id="numBeneficio2"]').text.strip()
    dados["nome"] = find_xpath(driver, '//*[@id="cliNome2"]').text.strip()
    dados["cpf"] = find_xpath(driver, '//*[@id="cliCpf2"]').text.strip()
    dados["nascimento"] = find_xpath(driver, '//*[@id="cliNascimento"]').text.strip()

    dados["situacao_beneficio"] = find_xpath(
        driver, '//td[b[text()="Situação do Benefício"]]/following-sibling::td'
    ).text.strip()

    dados["uf_nb"] = find_xpath(
        driver, '//td[b[text()="NB - UF"]]/following-sibling::td'
    ).text.strip()

    dados["nascimento"] = find_xpath(
        driver, '//td[b[text()="Nascimento"]]/following-sibling::td'
    ).text.strip()

    dados["ddb"] = find_xpath(
        driver, '//td[b[text()="DDB"]]/following-sibling::td'
    ).text.strip()

    dados["especie"] = find_xpath(
        driver, '//td[b[text()="Espécie"]]/following-sibling::td'
    ).text.strip()

    dados["meio_pagamento"] = find_xpath(
        driver, '//td[b[text()="Meio Pagamento"]]/following-sibling::td'
    ).text.strip()

    dados["banco"] = find_xpath(
        driver, '//td[b[text()="Banco"]]/following-sibling::td'
    ).text.strip()

    dados["agencia"] = find_xpath(driver, '//*[@id="cliAgencia2"]').text.strip()
    dados["conta_corrente"] = find_xpath(driver, '//*[@id="cliConta2"]').text.strip()

    dados["endereco"] = find_xpath(
        driver, '//td[b[text()="Endereço"]]/following-sibling::td'
    ).text.strip()

    dados["cep"] = find_xpath(
        driver, '//td[b[text()="CEP"]]/following-sibling::td'
    ).text.strip()

    dados["bairro"] = find_xpath(
        driver, '//td[b[text()="Bairro"]]/following-sibling::td'
    ).text.strip()

    dados["cidade_uf"] = find_xpath(driver, '//*[@id="cliCidade"]').text.strip()

    dados["mr"] = find_xpath(
        driver,
        '//small[b[text()="MR"]]/ancestor::div[contains(@class,"dashboard-stat2")]//div[@class="progress-info"]/b'
    ).text.strip()

    dados["base_calculo"] = find_xpath(
        driver,
        '//small[b[text()="BASE DE CÁLCULO"]]/ancestor::div[contains(@class,"dashboard-stat2")]//div[@class="progress-info"]/b'
    ).text.strip()

    dados["margem_35"] = find_xpath(
        driver,
        '//small[b[contains(text(),"MARGEM 35")]]/ancestor::div[contains(@class,"dashboard-stat2")]//div[@class="progress-info"]/b'
    ).text.strip()

    dados["margem_ir"] = find_xpath(
        driver,
        '//small[b[contains(text(),"MARGEM IR")]]/ancestor::div[contains(@class,"dashboard-stat2")]//div[@class="progress-info"]/b'
    ).text.strip()

    dados["margem_cartao"] = find_xpath(
        driver,
        '//small[b[text()="MARGEM CARTÃO"]]/ancestor::div[contains(@class,"dashboard-stat2")]//div[@class="progress-info"]/b'
    ).text.strip()

    dados["cartao_beneficio"] = find_xpath(
        driver,
        '//small[b[text()="CARTÃO BENEFÍCIO"]]/ancestor::div[contains(@class,"dashboard-stat2")]//div[@class="progress-info"]/b'
    ).text.strip()

    try:
        dados["empréstimos"] = search_loans_data(driver)
    except:
        dados["cartões"] = "Cliente não possui empréstimos ativos"

    return dados


def search_loans_data(driver):
    loans = []

    div_propostas = find_xpath(driver, '//*[@id="form-propostas"]/div/section/div/div[1]')
    
    linhas = div_propostas.find_elements(
        By.XPATH, './/div[starts-with(@id,"linha_")]'
    )

    for linha in linhas:
        emprestimo = {}

        linha_id = linha.get_attribute("id")
        index = linha_id.split("_")[-1]

        emprestimo["banco"] = linha.find_element(
            By.XPATH, './/span[contains(@class,"linha__banco")]'
        ).text.strip()

        emprestimo["parcela"] = linha.find_element(
            By.XPATH, f'.//*[@id="valorParcelaEmp_{index}"]'
        ).text.strip()

        emprestimo["saldo_devedor"] = linha.find_element(
            By.XPATH, './/span[contains(.,"Saldo devedor")]/following-sibling::text()'
        ) if False else linha.find_element(
            By.XPATH, './/span[contains(.,"Saldo devedor")]/parent::span'
        ).text.replace("Saldo devedor:", "").strip()

        emprestimo["prazo"] = linha.find_element(
            By.XPATH, './/span[contains(.,"Prazo:")]'
        ).text.replace("Prazo:", "").strip()

        emprestimo["taxa"] = linha.find_element(
            By.XPATH, './/span[contains(.,"Taxa:")]'
        ).text.replace("Taxa:", "").strip()

        emprestimo["data_averbacao"] = linha.find_element(
            By.XPATH, './/span[contains(.,"Data Averbação:")]'
        ).text.replace("Data Averbação:", "").strip()

        emprestimo["contrato"] = linha.find_element(
            By.XPATH, './/span[contains(@class,"text--contrato")]'
        ).text.replace("Contrato:", "").strip()

        loans.append(emprestimo)

    return loans


