from sparkpost import SparkPost
import os
sparky = SparkPost() # uses environment variable
from_email = 'test@' + os.environ.get('SPARKPOST_SANDBOX_DOMAIN') # 'test@sparkpostbox.com'

response = sparky.transmission.send(
    use_sandbox=True,
    recipients=['raghunathan.karthik@gmail.com'],
    html='<html><body><p>Testing SparkPost - the world\'s most awesomest email service!</p></body></html>',
    from_email='kraghunathan@kraghunathan-C02Q4K2YG8WP.local',
    subject='Oh hey!'
)

print response

