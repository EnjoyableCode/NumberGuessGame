
case "$(pidof uwsgi | wc -w)" in

0)  echo "Not Found1" 
    /usr/local/bin/uwsgi --socket 0.0.0.0:8080 --chdir /home/putcurrentdirectoryhere --protocol=http -w uwsgi_handler
    ;;
1)  echo "Found1"
    ;;
*)  echo "2"
    ;;
esac
