<br/>
<p align="center">
  <a href="https://github.com/base4-offensive-operations/autolb-proxies">
    <img src="https://4.bp.blogspot.com/-a_5SXSkmbT0/Wb_dfwCEvTI/AAAAAAAAJP4/UN8oJorMU_c4o8dl8DaFC-4uTQOwzRBegCLcBGAs/s1600/Captura%2Bde%2Bpantalla%2B2017-09-18%2Ba%2Blas%2B11.50.36%2Ba.m..png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">AutoLB-Proxies</h3>

  <p align="center">
    From proxy list to load balancer using go-dispatch-proxy :)
    <br/>
    <br/>
    <a href="https://github.com/base4-offensive-operations/autolb-proxies/issues">Request Feature</a>
  </p>
</p>

![Stargazers](https://img.shields.io/github/stars/base4-offensive-operations/autolb-proxies?style=social) ![Issues](https://img.shields.io/github/issues/base4-offensive-operations/autolb-proxies) ![License](https://img.shields.io/github/license/base4-offensive-operations/autolb-proxies) 

## About The Project

Herramienta desarrollada para la automatización de scraping de proxies publicos, verificar su estado y luego levantar un load balancer. Para así crear un proxy rotativo socks5 con el cual podemos escanear puertos, realizar web scraping, etc.

## Built With

- Python3
- https://github.com/extremecoders-re/go-dispatch-proxy

## Getting Started


### Prerequisites

Este proyecto utiliza go-dispatch-proxy, puedes descargar el binario desde su repo o compilar el código fuente. Al obtener el binario, debes moverlo a la carpeta de este proyecto o editar la línea 183 del script con la ruta del binario. 
También debes ejecutar "./loadbalancer -list" para revisar que interfaces/ip es posible utilizar para levantar el lb, una vez desplegada la lista, editas la linea 183 con el IP donde quieras levantar el loadbalancer con el puerto por defecto en 8080.

### Installation


```sh
pip3 install colored
git clone https://github.com/base4-offensive-operations/autolb-proxies.git
```

## Usage

- Traer todos los proxies del tipo socks5, con latencia menor a 50ms y levantar un load balancer:
```sh
python3 autolb-proxies.py --type socks5 --latency 50 --webtest http://ifconfig.me/ip --lbproxies
```

- Traer todos los proxies del tipo socks5, con latencia menor a 100ms y crear el archivo de configuración de proxychains:
```sh
python3 autolb-proxies.py --type socks5 --webtest http://ifconfig.me/ip --proxychains
```

- Traer todos los proxies del tipo socks5, con latencia menor a 100ms y crear el archivo de configuración de proxychains, y setear encadenamiento de conexión de 2 proxies:
```sh
python3 autolb-proxies.py --type socks5 --webtest http://ifconfig.me/ip --proxychains --chainlength 2
```

- Traer todos los proxies del tipo https, con latencia menor a 100ms e imprimir solo el IP:PUERTO
```sh
python3 autolb-proxies.py --type https --webtest http://ifconfig.me/ip --onlyip
```

## License

Distributed under the MIT License. See [LICENSE](https://github.com/base4-offensive-operations/autolb-proxies/blob/main/LICENSE.md) for more information.

## Authors

* **Juan Cruz Tommasi** - *Ethical Hacking & Research* - [@jc-base4sec](https://github.com/jc-base4sec) - **
