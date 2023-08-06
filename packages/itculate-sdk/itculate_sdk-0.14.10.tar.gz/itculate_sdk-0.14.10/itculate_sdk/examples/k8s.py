import datetime

from unix_dates import UnixDate

import itculate_sdk as itsdk

itsdk.init(provider="Print",
           api_key="b8NgSwETBuaFR30L3a8JP0F5NwJ55Ale",
           api_secret="zVZYK-w-UEP_aqFUSN7AWvsEFmYffnbaT_sHRcSamit73pZVJWy0eS2lrny6sC7c")

#############################
# create topology
#############################

collector_id = "kubernetes"

kubernetes = itsdk.add_vertex(name="lab-cluster",
                              vertex_type="Kubernetes",
                              keys="kubernetes-cluster",
                              collector_id=collector_id,
                              data={
                                  "attr1": "attr_value_1",
                                  "attr2": "attr_value_2",
                              })

node1 = itsdk.add_vertex(name="node1",
                         vertex_type="EC2",
                         keys="i-1000001",
                         collector_id=collector_id,
                         data={
                             "attr1": "attr_value_1",
                             "attr2": "attr_value_2",
                         })

node2 = itsdk.add_vertex(name="node1",
                         vertex_type="EC2",
                         keys="i-1000002",
                         collector_id=collector_id,
                         data={
                             "attr1": "attr_value_1",
                             "attr2": "attr_value_2",
                         })

container = itsdk.add_vertex(name="container1",
                             vertex_type="Docker",
                             keys="container-1",
                             collector_id=collector_id,
                             data={
                                 "attr1": "attr_value_1",
                                 "attr2": "attr_value_2",
                             })

pods_cluster1 = itsdk.add_vertex(name="pod-config-1",
                                 vertex_type="Cluster",
                                 keys="pods-config-1",
                                 collector_id=collector_id,
                                 data={
                                     "attr1": "attr_value_1",
                                     "attr2": "attr_value_2",
                                 })

pods_cluster2 = itsdk.add_vertex(name="pod-config-2",
                                 vertex_type="Cluster",
                                 keys="pods-config-2",
                                 collector_id=collector_id,
                                 data={
                                     "attr1": "attr_value_1",
                                     "attr2": "attr_value_2",
                                 })

itsdk.connect(source=kubernetes,
              target=[node1, node2],
              topology="use-ec2",
              collector_id=collector_id)

itsdk.connect(source=kubernetes,
              target=[pods_cluster1, pods_cluster2],
              topology="configured-pods",
              collector_id=collector_id)

itsdk.connect(source=[pods_cluster1, pods_cluster2],
              target=[node1, node2],
              topology="pods-use-ec2",
              collector_id=collector_id)
#
# now = int(UnixDate.now())
# for i in range(now - 60 * 60 * 10, now, 15*60):
#     itsdk.add_sample(vertex="pods-config-1",
#                      counter="latency",
#                      value=itsdk.LatencyDataType.value(i%10),
#                      timestamp=i
#                      )

topology = {
    'collector_id': 'collector-1',
    'tenant_id': "tenant-1",
    'vertices': [
        {
            '_keys': {'pk': 'i-1000002'},
            '_name': 'node1',
            '_type': 'EC2',
            'attr1': 'attr_value_1',
            'attr2': 'attr_value_2',
        },
        {'_keys': {'pk': 'kubernetes-cluster'},
         '_name': 'lab-cluster',
         '_type': 'Kubernetes',
         'attr1': 'attr_value_1',
         'attr2': 'attr_value_2',
         },
        {'_keys': {'pk': 'container-1'},
         '_name': 'container1',
         '_type': 'Docker',
         'attr1': 'attr_value_1',
         'attr2': 'attr_value_2',
         },
        {'_keys': {'pk': 'i-1000001'},
         '_name': 'node1',
         '_type': 'EC2',
         'attr1': 'attr_value_1',
         'attr2': 'attr_value_2',
         },
        {'_keys': {'pk': 'pods-config-1'},
         '_name': 'pod-config-1',
         '_type': 'Cluster',
         'attr1': 'attr_value_1',
         'attr2': 'attr_value_2',
         },
        {'_keys': {'pk': 'pods-config-2'},
         '_name': 'pod-config-2',
         '_type': 'Cluster',
         'attr1': 'attr_value_1',
         'attr2': 'attr_value_2',
         }],
    'edges': [
        {
            '_source_keys': {'pk': 'kubernetes-cluster'},
            '_target_keys': {'pk': 'i-1000001'},
            '_type': 'use-ec2'
        },
        {
            '_source_keys': {'pk': 'kubernetes-cluster'},
            '_target_keys': {'pk': 'i-1000002'},
            '_type': 'use-ec2'
        },
        {
            '_source_keys': {'pk': 'kubernetes-cluster'},
            '_target_keys': {'pk': 'pods-config-1'},
            '_type': 'configured-pods'
        },
        {
            '_source_keys': {'pk': 'kubernetes-cluster'},
            '_target_keys': {'pk': 'pods-config-2'},
            '_type': 'configured-pods'
        },
        {
            '_source_keys': {'pk': 'pods-config-1'},
            '_target_keys': {'pk': 'i-1000001'},
            '_type': 'pods-use-ec2'
        },
        {
            '_source_keys': {'pk': 'pods-config-1'},
            '_target_keys': {'pk': 'i-1000002'},
            '_type': 'pods-use-ec2'
        },
        {
            '_source_keys': {'pk': 'pods-config-2'},
            '_target_keys': {'pk': 'i-1000001'},
            '_type': 'pods-use-ec2'
        },
        {
            '_source_keys': {'pk': 'pods-config-2'},
            '_target_keys': {'pk': 'i-1000002'},
            '_type': 'pods-use-ec2'
        }],
}


itsdk.flush_all()
