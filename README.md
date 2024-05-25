# Input Stats

Input Stats is a Home Assistant component that allows you to create your own sensors to store your own statistics and manage them manually.

Thanks to the various Home Assistant options, we can later consult the evolution of our data by comparing it over different periods.


## Installation

You can install the component using HACS or download manually in you Home Assistant configuration directory.

## Configuration

To add a new configuration, go to `Settings -> Devices & Services -> Add Integration -> Input Stats`.

You will be prompted to fill in the following fields:

- **Name:** Name of your sensor
- **Type:** Type of statistics to store
  - **Measurement:** Used when we are interested in the different values of our sensor. Useful for information where we are interested in its evolution, such as prices, temperatures, weights...
  - **Total:** Used when the values are cumulative. For example, car mileage, accumulated bill expenses, actions performed...
- **Unit of measurement:** Unit of your sensor, it can be liters (l), kilograms (kg), euros (€). If it is a simple counter, no unit can be set.

It is especially useful for keeping a historical record of data such as bills, car mileage, number of times you go to the gym...

To change the sensor values, there are 3 services available which can be used both manually and from automations.

## Set Value
This service allows you to specify the new value of the sensor. For example, it allows you to indicate your current weight or the car's mileage.

```yaml
service: input_stats.set_value
target:
  entity_id: sensor.i40_odometer
data:
  amount: 75000
```

## Increment
This service allows you to add a specific amount to the sensor. For example, when a new bill arrives, you only need to indicate the cost of that bill to keep track of the total cost.

```yaml
service: input_stats.increment
target:
  entity_id: sensor.water_bill
data:
  amount: 30
  
```

## Decrement
This service allows you to subtract a specific amount from the sensor. For example, when a refund arrives, you only need to indicate the cost of that bill, and it will be deducted.

```yaml
service: input_stats.decrement
target:
  entity_id: sensor.water_bill
data:
  amount: 3
```