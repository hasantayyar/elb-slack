import boto3
import tzlocal
import datetime

ec2 = boto3.resource('ec2')
auto_scale = boto3.client('autoscaling')


'''
get all instances with given autoscale group name
'''
def get_instances(autoscale_group_name):
    instances = []
    ag = auto_scale.describe_auto_scaling_groups(AutoScalingGroupNames=[autoscale_group_name], MaxRecords=1)
    for i in ag["AutoScalingGroups"][0]["Instances"]:
        if i["HealthStatus"] == "Healthy" and i["LifecycleState"] == "InService":
            instances.append(ec2.Instance(i["InstanceId"]))
    return instances


'''
get an instance's uptime secons as secons since last payment
'''
def seconds_since_last_payment(instance):
    now = datetime.datetime.now(tzlocal.get_localzone())
    itime = instance.launch_time
    return (now - itime).total_seconds() % 3600

'''
sort instances by uptime seconds
'''
def get_sorted_instances(instances):
    return sorted(instances, key=lambda x: seconds_since_last_payment(x), reverse=True)

def get_instances_with_tag(tag):
    instances = ec2.instances.filter(Filters=[
        {
            'Name': 'tag',
            'Values': [tag]
        },
    ])
    return list(instances)


def terminate_instance(id_str):
    #will also decrement desired capacity
    return auto_scale.terminate_instance_in_auto_scaling_group(
        InstanceId=id_str,
        ShouldDecrementDesiredCapacity=True
    )


def get_auto_scale_group(autoscale_group_name):
    ag = auto_scale.describe_auto_scaling_groups(AutoScalingGroupNames=[autoscale_group_name], MaxRecords=1)
    if len(ag["AutoScalingGroups"]) > 0:
        return ag["AutoScalingGroups"][0]
    return False


def set_desired_capacity(capacity, autoscale_group_name):
    return auto_scale.set_desired_capacity(
        AutoScalingGroupName=autoscale_group_name,
        DesiredCapacity=capacity,
        HonorCooldown=False
    )


def get_desired_capacity():
    ag = get_auto_scale_group()
    if ag:
        return ag["DesiredCapacity"]
    return 0
