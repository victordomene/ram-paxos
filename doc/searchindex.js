Search.setIndex({envversion:46,filenames:["index","modules","paxos","paxos.messengers","paxos.protobufs","paxos.rdtp","paxos.receivers"],objects:{"":{paxos:[2,0,0,"-"]},"paxos.acceptor":{Acceptor:[2,3,1,""]},"paxos.acceptor.Acceptor":{handle_accept:[2,2,1,""],handle_prepare:[2,2,1,""]},"paxos.learner":{Learner:[2,3,1,""]},"paxos.learner.Learner":{handle_diff_file:[2,2,1,""],handle_learn:[2,2,1,""],handle_print_difference_mean:[2,2,1,""],handle_print_differences:[2,2,1,""],handle_print_ledger:[2,2,1,""],write_to_ledger:[2,2,1,""]},"paxos.messengers":{messenger:[3,0,0,"-"],rdtpMessenger:[3,0,0,"-"],rpcMessenger:[3,0,0,"-"]},"paxos.messengers.messenger":{Messenger:[3,3,1,""]},"paxos.messengers.messenger.Messenger":{add_destination:[3,2,1,""],fetch_proposal:[3,2,1,""],get_quorum:[3,2,1,""],send_accept:[3,2,1,""],send_learn:[3,2,1,""],send_prepare:[3,2,1,""],send_promise:[3,2,1,""],send_refuse:[3,2,1,""],stamp_proposal:[3,2,1,""]},"paxos.messengers.rdtpMessenger":{rdtpMessenger:[3,3,1,""]},"paxos.messengers.rdtpMessenger.rdtpMessenger":{add_destination:[3,2,1,""],connect:[3,2,1,""],get_quorum:[3,2,1,""],send_accept:[3,2,1,""],send_learn:[3,2,1,""],send_prepare:[3,2,1,""],send_promise:[3,2,1,""],send_refuse:[3,2,1,""],try_send:[3,2,1,""]},"paxos.messengers.rpcMessenger":{grpcMessenger:[3,3,1,""],ignore:[3,1,1,""],ignore_accept:[3,1,1,""],ignore_learn:[3,1,1,""],ignore_promise:[3,1,1,""],ignore_refuse:[3,1,1,""]},"paxos.messengers.rpcMessenger.grpcMessenger":{add_destination:[3,2,1,""],get_quorum:[3,2,1,""],send_accept:[3,2,1,""],send_learn:[3,2,1,""],send_prepare:[3,2,1,""],send_promise:[3,2,1,""],send_refuse:[3,2,1,""]},"paxos.proposal":{Proposal:[2,3,1,""]},"paxos.proposer":{Proposer:[2,3,1,""]},"paxos.proposer.Proposer":{handle_promise:[2,2,1,""],handle_refuse:[2,2,1,""],propose:[2,2,1,""]},"paxos.protobufs":{paxos_pb2:[4,0,0,"-"]},"paxos.protobufs.paxos_pb2":{BetaVMServicer:[4,3,1,""],BetaVMStub:[4,3,1,""],beta_create_VM_server:[4,1,1,""],beta_create_VM_stub:[4,1,1,""]},"paxos.protobufs.paxos_pb2.BetaVMServicer":{handle_accept:[4,2,1,""],handle_learn:[4,2,1,""],handle_prepare:[4,2,1,""],handle_promise:[4,2,1,""],handle_refuse:[4,2,1,""]},"paxos.protobufs.paxos_pb2.BetaVMStub":{handle_accept:[4,2,1,""],handle_learn:[4,2,1,""],handle_prepare:[4,2,1,""],handle_promise:[4,2,1,""],handle_refuse:[4,2,1,""]},"paxos.rdtp":{rdtp:[5,0,0,"-"]},"paxos.rdtp.rdtp":{ClientDead:[5,4,1,""],ServerDead:[5,4,1,""],recv:[5,1,1,""],recv_message:[5,1,1,""],recv_nbytes:[5,1,1,""],send:[5,1,1,""],send_message:[5,1,1,""]},"paxos.receivers":{rdtpReceiver:[6,0,0,"-"],receiver:[6,0,0,"-"],rpcReceiver:[6,0,0,"-"]},"paxos.receivers.rdtpReceiver":{rdtpReceiver:[6,3,1,""]},"paxos.receivers.rdtpReceiver.rdtpReceiver":{handle_accept:[6,2,1,""],handle_diff_file:[6,2,1,""],handle_learn:[6,2,1,""],handle_prepare:[6,2,1,""],handle_print_differences:[6,2,1,""],handle_print_ledger:[6,2,1,""],handle_promise:[6,2,1,""],handle_refuse:[6,2,1,""],serve:[6,2,1,""],stop_server:[6,2,1,""],usage_args:[6,2,1,""]},"paxos.receivers.receiver":{Receiver:[6,3,1,""]},"paxos.receivers.receiver.Receiver":{handle_accept:[6,2,1,""],handle_learn:[6,2,1,""],handle_prepare:[6,2,1,""],handle_promise:[6,2,1,""],handle_refuse:[6,2,1,""],serve:[6,2,1,""]},"paxos.receivers.rpcReceiver":{grpcReceiver:[6,3,1,""]},"paxos.receivers.rpcReceiver.grpcReceiver":{handle_accept:[6,2,1,""],handle_learn:[6,2,1,""],handle_prepare:[6,2,1,""],handle_promise:[6,2,1,""],handle_refuse:[6,2,1,""],serve:[6,2,1,""],stop_server:[6,2,1,""]},"paxos.vm":{VM:[2,3,1,""]},"paxos.vm.VM":{add_destination:[2,2,1,""],propose_to_quorum:[2,2,1,""],serve:[2,2,1,""],stop_server:[2,2,1,""]},paxos:{acceptor:[2,0,0,"-"],learner:[2,0,0,"-"],messengers:[3,0,0,"-"],proposal:[2,0,0,"-"],proposer:[2,0,0,"-"],protobufs:[4,0,0,"-"],rdtp:[5,0,0,"-"],receivers:[6,0,0,"-"],vm:[2,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","method","Python method"],"3":["py","class","Python class"],"4":["py","exception","Python exception"]},objtypes:{"0":"py:module","1":"py:function","2":"py:method","3":"py:class","4":"py:exception"},terms:{"abstract":[2,3,6],"case":2,"class":[2,3,4,6],"function":[2,3,4,6],"new":2,"return":[2,3,6],"true":[2,3],abort:2,accept:[2,3,6],acceptor:1,access:[3,6],accordingli:2,actual:2,add:[2,3,6],add_destin:[2,3],after:3,algorithm:2,all:[3,6],allow:[2,3,6],alreadi:[2,3],also:[2,3],alwai:2,ani:[2,3],anoth:2,anyth:2,anywai:2,appropri:[2,6],arg:[3,5],argument:[3,6],assign:[3,6],associ:3,back:[3,6],base:[3,4,5,6],basic:3,becaus:3,been:[2,3],below:2,benchmark:[2,3],beta_create_vm_serv:4,beta_create_vm_stub:4,betavmservic:4,betavmstub:4,between:2,book:6,both:2,call:[2,3],can:[2,3],cannot:[2,6],channel:4,chat:[3,6],check:[2,6],chosen:2,clientdead:5,combin:3,commun:[3,6],connect:3,contain:3,content:1,context:[4,6],correspond:2,could:2,cs262:[3,6],current:[2,6],decre:[2,3,6],default_timeout:4,defin:[3,4,6],describ:2,dest:3,destin:[2,3],dictionari:[2,3],diff_fil:6,differ:[2,3,6],disk:2,doe:[2,6],each:3,enough:[2,6],event:2,everi:2,everybodi:3,everyon:[3,6],except:5,exclus:[3,6],exist:[2,3],expect:6,fals:[2,3],far:6,fetch_propos:3,file:2,found:3,from:3,futur:3,get_quorum:3,given:[2,3,6],googl:[3,6],grpc:[3,6],grpcmesseng:3,grpcreceiv:6,guarante:3,had_previ:[3,6],handl:[2,6],handle_accept:[2,4,6],handle_diff_fil:[2,6],handle_learn:[2,4,6],handle_prepar:[2,4,6],handle_print_differ:[2,6],handle_print_difference_mean:2,handle_print_ledg:[2,6],handle_promis:[2,4,6],handle_refus:[2,4,6],have:[2,6],here:2,high:[3,6],higher:[2,3],highest:[2,3],host:[2,3,4,6],ignor:3,ignore_accept:3,ignore_learn:3,ignore_promis:3,ignore_refus:3,implement:[2,3,6],includ:6,index:[0,3],inform:3,initi:2,instanc:[2,6],instead:2,interfac:[2,3,6],intern:2,issu:6,keep:[2,6],lamport:2,law:6,learn:2,learner:1,learnrequest:6,learnt:2,ledger:2,less:3,level:[3,6],list:3,lot:2,lower:2,machin:[2,3,6],made:[2,3],mai:[2,3,6],major:3,map:2,maximum_timeout:4,mean:2,messag:[3,5],messeng:1,messengerclass:2,metadata_transform:4,method:[3,6],middl:2,modul:1,must:[2,3,6],name:[2,3],necessari:[2,6],need:[2,3,6],network:2,none:[2,3,4],noth:6,notic:[2,3,6],num:6,number:[2,3],object:[2,4],onli:2,optim:2,other:2,otherwis:[2,3],our:[2,3,6],out:2,own:[3,6],packag:1,page:0,param:[2,3,6],paramet:2,pass:2,past:2,paxon:2,paxos_pb2:1,peopl:6,place:2,pool:4,pool_siz:4,port:[2,3,6],possibl:3,prepar:[2,3,6],present:[3,6],previou:2,print:2,print_differ:6,print_ledg:6,probabl:3,promis:[2,3,6],propos:1,propose_to_quorum:2,protobuf:1,protocol:[3,6],provid:[3,4,6],purpos:3,question:[2,3],quorum:[2,3,6],rdtp:[1,3],rdtpmesseng:1,rdtpreceiv:1,reason:[3,6],receiv:[1,4],receiverclass:2,recv:5,recv_messag:5,recv_nbyt:5,refer:[2,3,6],refus:[2,6],request:[2,3,4,6],respond:[2,3,6],retriev:3,rpc:[3,6],rpcmesseng:1,rpcreceiv:1,run:6,sai:3,same:2,search:0,second:3,see:[2,3],seen:6,send:[2,3,5,6],send_accept:3,send_learn:3,send_messag:5,send_prepar:3,send_promis:3,send_refus:3,sent:[2,3],serv:[2,6],server:[2,6],serverdead:5,servic:4,set:3,should:[3,6],simpli:[2,3],sinc:2,singl:[3,6],sock:5,some:[2,3,6],specif:[3,6],specifi:2,stamp_propos:3,start:[2,6],statu:5,step:2,stop:[2,6],stop_serv:[2,6],store:3,stub:3,submodul:1,subpackag:1,succe:2,success:2,successfulli:3,suppos:2,synod:2,take:[3,6],taken:3,tell:3,than:[2,3],thei:[3,6],them:[3,6],therefor:6,thi:[2,3,6],timeout:4,timestamp:3,track:[2,6],try_send:3,type:[3,6],unless:2,updat:[2,3],usage_arg:6,use_disk:2,valu:[2,3,6],virtual:2,vote:[2,3],what:[3,6],when:2,where:3,which:[2,3,4,6],who:[2,3],whom:[2,3],work:2,would:2,write:2,write_to_ledg:2,wrote:[3,6]},titles:["Welcome to RAM-ified Part-Time Parliament&#8217;s documentation!","paxos","paxos package","paxos.messengers package","paxos.protobufs package","paxos.rdtp package","paxos.receivers package"],titleterms:{acceptor:2,content:[2,3,4,5,6],document:0,ifi:0,indic:0,learner:2,messeng:3,modul:[2,3,4,5,6],packag:[2,3,4,5,6],parliament:0,part:0,paxo:[1,2,3,4,5,6],paxos_pb2:4,propos:2,protobuf:4,ram:0,rdtp:5,rdtpmesseng:3,rdtpreceiv:6,receiv:6,rpcmesseng:3,rpcreceiv:6,submodul:[2,3,4,5,6],subpackag:2,tabl:0,time:0,welcom:0}})