const selectorAll = document.querySelectorAll.bind(document);
const id = document.getElementById.bind(document);
function mascara(o,f){
  obj=o
  fun=f
  setTimeout("execmascara()",1)
}
function execmascara(){
  obj.value=fun(obj.value)
}
function mtel(v){
  v=v.replace(/\D/g,"");                  //Remove tudo o que não é dígito
  v=v.replace(/^(\d{2})(\d)/g,"($1)$2");  //Coloca parênteses em volta dos dois primeiros dígitos
  v=v.replace(/(\d)(\d{4})$/,"$1-$2");    //Coloca hífen entre o quarto e o quinto dígitos
  return v;
}
function validaCPF(v){
  v=v.replace(/\D/g,"");//Remove tudo o que não é dígito
  v=v.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g,"$1.$2.$3-$4");
  return v;
}
function validaCEP(v){
  v=v.replace(/\D/g,"");//Remove tudo o que não é dígito
  v=v.replace(/^(\d{5})(\d{3})$/g,"$1-$2");
  return v;
}
function validaCNPJ(v){
  v=v.replace(/\D/g,"");//Remove tudo o que não é dígito
  //Coloca ponto entre o segundo e o terceiro dígitos
  v=v.replace(/^(\d{2})(\d)/, "$1.$2")
  //Coloca ponto entre o quinto e o sexto dígitos
  v=v.replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
  //Coloca uma barra entre o oitavo e o nono dígitos
  v=v.replace(/\.(\d{3})(\d)/, ".$1/$2")
  //Coloca um hífen depois do bloco de quatro dígitos
  v=v.replace(/(\d{4})(\d)/, "$1-$2")
  return v;
}

window.onload = function(){
  let CPF = selectorAll(".CPF");
  for (let i = 0; i < CPF.length; i++) {
    CPF[i].onkeyup = function(){
      mascara( this, validaCPF );
    }
  }
  let cnpj = selectorAll(".cnpj");
  for (let i = 0; i < cnpj.length; i++) {
    cnpj[i].onkeyup = function(){
      mascara( this, validaCNPJ );
    }
  }
  let numero = selectorAll(".telefone");
  for (let i = 0; i < numero.length; i++) {
    numero[i].onkeyup = function(){
      mascara( this, mtel );
    }
  }
  let CEP = id("CEP");
  CEP.onkeyup = function(){
    mascara( this, validaCEP);
  }
}

function validacao(telefone){
  //retira todos os caracteres menos os numeros
  telefone = telefone.replace(/\D/g,'');
  //verifica se tem a quantidade de numeros correta
  if(!(telefone.length >= 10 && telefone.length <= 11)) return false;
  //Verifica se o DDD é válido
  if(parseInt(telefone.substring(0, 1)) == 0 || parseInt(telefone.substring(1, 2)) == 0) return false;
  //Se tiver 11 caracteres, verificar se começa com 9
  if(telefone.length == 11 && parseInt(telefone.substring(2, 3)) != 9) return false;
  //Se tiver 11 caracteres, verifica se o 4° digito está correto
  if(telefone.length == 11 && [6, 7, 8, 9].indexOf(parseInt(telefone.substring(3, 4))) == -1) return false;
  //Se tiver 10 caracteres, verifica se o 3° digito está correto
  if(telefone.length == 10 && [2, 3, 4, 5].indexOf(parseInt(telefone.substring(2, 3))) == -1) return false;
  return true;
}
function testaCPF(strCPF) {
  strCPF=strCPF.replace(/\D/g,"");//Remove tudo o que não é dígito
    let soma = 0;
    let resto;
	if (strCPF == "00000000000") return false;

	for (i=1; i<=9; i++) soma += parseInt(strCPF.substring(i-1, i)) * (11 - i);
	resto = (soma * 10) % 11;
	
  if ((resto == 10) || (resto == 11))  resto = 0;
  if (resto != parseInt(strCPF.substring(9, 10))) return false;
	
	soma = 0;
  for (i = 1; i <= 10; i++) soma += parseInt(strCPF.substring(i-1, i)) * (12 - i);
  resto = (soma * 10) % 11;
	
  if ((resto == 10) || (resto == 11))  resto = 0;
  if (resto != parseInt(strCPF.substring(10, 11))) return false;
  return true;
}
function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, '');
    if(cnpj == '') return false;
    if (cnpj.length != 14)
        return false;
    // Elimina CNPJs invalidos conhecidos
    if (cnpj == "00000000000000" || 
        cnpj == "11111111111111" || 
        cnpj == "22222222222222" || 
        cnpj == "33333333333333" || 
        cnpj == "44444444444444" || 
        cnpj == "55555555555555" || 
        cnpj == "66666666666666" || 
        cnpj == "77777777777777" || 
        cnpj == "88888888888888" || 
        cnpj == "99999999999999")
        return false;
    // Valida DVs
    let tamanho = cnpj.length - 2
    let numeros = cnpj.substring(0,tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(0))
        return false;
    tamanho = tamanho + 1;
    numeros = cnpj.substring(0,tamanho);
    soma = 0;
    pos = tamanho - 7;
    for (i = tamanho; i >= 1; i--) {
      soma += numeros.charAt(tamanho - i) * pos--;
      if (pos < 2)
            pos = 9;
    }
    resultado = soma % 11 < 2 ? 0 : 11 - soma % 11;
    if (resultado != digitos.charAt(1))
          return false;
    return true;
}
function limpa_formulário_CEP() {
  //Limpa valores do formulário de cep.
  id('rua').value=("");
  id('bairro').value=("");
  id('cidade').value=("");
  id('uf').value=("");
  id('ibge').value=("");
}
function meu_callback(conteudo) {
  if (!("erro" in conteudo)) {
    //Atualiza os campos com os valores.
    id('rua').value=(conteudo.logradouro);
    id('bairro').value=(conteudo.bairro);
    id('cidade').value=(conteudo.localidade);
    id('uf').value=(conteudo.uf);
    id('ibge').value=(conteudo.ibge);
  } //end if.
  else {
    //CEP não Encontrado.
    limpa_formulário_CEP();
    respostaCEP.style.display = "block";
    respostaCEP.innerHTML = "CEP não encontrado."
  }
}
function pesquisaCEP(valor) {
  //Preenche os campos com "..." enquanto consulta webservice.
  /**
  document.getElementById('rua').value="...";
  document.getElementById('bairro').value="...";
  document.getElementById('cidade').value="...";
  document.getElementById('uf').value="...";
  document.getElementById('ibge').value="...";
  */
  //Nova variável "cep" somente com dígitos.
  let CEP = valor.replace(/\D/g, '');
  //Verifica se campo cep possui valor informado.
  if (CEP != "") {
    //Expressão regular para validar o CEP.
    let validaCEP = /^[0-9]{8}$/;
    //Valida o formato do CEP.
    if(validaCEP.test(CEP)) {
      //Cria um elemento javascript.
      let script = document.createElement('script');
      //Sincroniza com o callback.
      script.src = 'https://viacep.com.br/ws/'+ CEP + '/json/?callback=meu_callback';
      //Insere script no documento e carrega o conteúdo.
      document.body.appendChild(script);
      respostaCEP.style.display = "none";
      respostaCEP.innerHTML = ""
    } //end if.
    else {
      //cep é inválido.
      limpa_formulário_CEP();
      respostaCEP.style.display = "block";
      respostaCEP.innerHTML = "Formato de CEP inválido."
    }
  } //end if.
  else {
    //cep sem valor, limpa formulário.
    limpa_formulário_CEP();
  }
}

cadastro.CEP.onblur = function(){ var CEP = id("CEP"); pesquisaCEP(CEP.value);}

cadastro.onsubmit = function(){
  let respostaTel = id("respostaTel");
  let numero = selectorAll(".telefone");
  for (let i = 0; i < numero.length; i++) {
    if(validacao(numero[i].value) == false){
      respostaTel.style.display = "block";
      respostaTel.innerHTML = "O número digitado não existe";
      return false;
    }else{respostaTel.innerHTML = "";}
  }
  let respostaCPF = id("respostaCPF");
  let cpf = selectorAll(".cpf");
  for (let i = 0; i < cpf.length; i++) {
    if(testaCPF(cpf[i].value) == false){
      respostaCPF.style.display = "block";
      respostaCPF.innerHTML = "O CPF digitado não existe";
      return false;
    }else{respostaCPF.innerHTML = "";}
  }
  let respostaCNPJ = id("respostaCNPJ");
  let cnpj = selectorAll(".cnpj");
  for (let i = 0; i < cnpj.length; i++) {
    if(validarCNPJ(cnpj[i].value) == false){
      respostaCNPJ.style.display = "block";
      respostaCNPJ.innerHTML = "O CNPJ digitado não existe";
      return false;
    }else{respostaCNPJ.innerHTML = "";}
  }
  return true;
}