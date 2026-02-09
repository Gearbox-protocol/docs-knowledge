# How to pause contracts

{% stepper %}
{% step %}
### Navigate to emergency dashboard & Select Curator

[https://safe.gearbox.finance/emergency/](https://safe.gearbox.finance/emergency/)
{% endstep %}

{% step %}
### Pause needed contracts

<figure><img src="../../.gitbook/assets/Screenshot 2026-02-09 at 11.42.53.png" alt=""><figcaption></figcaption></figure>

* `Pause CM`
  * Forbid all operations with credit accounts within a CM
  * Liquidations are allowed to whitelisted emergency liquidators
* `Pause pool`
  * _Forbid deposits and withdrawals_
* `Pause market`
  * _Pause pool and all CMs_
* `Pause all contracts`
  * _For each market:_
    * _Pause pool and all CMs_
{% endstep %}
{% endstepper %}
