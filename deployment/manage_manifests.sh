# #!/bin/bash

# kubectl apply -f ingress.yml
# kubectl apply -f backend_weather.yml
# kubectl apply -f logger_weather.yml
# kubectl apply -f noti_weather.yml
# kubectl apply -f predict_weather.yml

# echo "Applied successfully!"

#!/bin/bash

# Function to apply the manifests
apply_manifests() {
    echo "Applying..."
    kubectl apply -f ingress.yml
    kubectl apply -f backend_weather.yml
    kubectl apply -f logger_weather.yml
    kubectl apply -f noti_weather.yml
    kubectl apply -f predict_weather.yml
    echo "Applied successfully!"
}

# Function to delete the manifests
delete_manifests() {
    echo "Deleting..."
    kubectl delete -f ingress.yml
    kubectl delete -f backend_weather.yml
    kubectl delete -f logger_weather.yml
    kubectl delete -f noti_weather.yml
    kubectl delete -f predict_weather.yml
    echo "Deleted successfully!"
}

# Check for the argument
if [[ $# -eq 0 ]]; then
  echo "Usage: $0 [apply|delete]"
  exit 1
fi

# Execute based on the argument
case $1 in
  apply)
    apply_manifests
    ;;
  delete)
    delete_manifests
    ;;
  *)
    echo "Invalid option. Use 'apply' to apply or 'delete' to delete the manifests."
    exit 1
    ;;
esac
