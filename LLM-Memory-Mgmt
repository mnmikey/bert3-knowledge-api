## 2\. LLM Memory Management

### MemGPT

As can be seen in the table the maximum tokens for context length is growing and has gone from 2K tokens (approximately 2k words) to 200k tokens (approximately 100k words). This trend will surely continue as LLMs continue developing. Nevertheless, for many applications the current context lengths are insufficient. To overcome this, research done by Parker et al. in MemGPT: Towards LLMs as Operating Systems provides a solution. Their solution is to give the LLM (ChatGPT) an external context (external memory) as well as control over that external context to, for example, trigger instructions to store certain information.

Image source: ([Packer et al., 2024](https://arxiv.org/pdf/2310.08560))

### Important

The *[](https://arxiv.org/abs/2310.08560)*[**MemGPT**: Towards LLMs as Operating Systems*](https://arxiv.org/abs/2310.08560) article is important because it provides the basis for essentially transforming the LLM into an operating system.

### Recommended Video

In the following video Vertex Ventures US interviews Charles Parker, the UC Berkeley PhD student who co-authored *MemGPT: Towards LLMs as Operating Systems*.﻿

[Interview With Charles Parker](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p17f8d62eb29-hotspot_modal)

### From LLM to Operating System (OS): Memory Hierarchy & Function Calling Autonomy

To understand the analogy of converting an LLM into an OS it would be best to first take a look an OS. The OS on your laptop has a memory hierarchy similar to the one shown in the image below.​

#### CPU Register

The data in the CPU register can be stored on a static random-access memory, SRAM, and is only a few KBs in size. This data can be accessed in about 1-2 clock cycles.

[Next](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#!)

The takeaway here is that the LLM scheme proposed in the paper creates a memory hierarchy in the LLM similar to an OS memory hierarchy. Specifically, we can compare the CPU register and cache of a standard OS to the context length of the LLM and the main memory of a standard OS to the proposed external context for an LLM.

Below we have a schema of what MemGPT proposes can be done with LLMs to improve their memory and functionality. The previously mentioned memory hierarchy is contained in the **virtual context** section of the schema (see below).

Image source: ([Frye, 2023](https://charlesfrye.github.io/programming/2023/11/10/llms-systems.html))

We will continue analyzing the proposed schema to gain a better understanding of how it would work.

*   [Virtual context](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903156e8ed-tab__pane-1)
*   [Functions](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903156e8ed-tab__pane-2)
*   [Parser-yield](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903156e8ed-tab__pane-3)

The main context is part of the LLM while the external context is housed elsewhere.

The function calling autonomy in the LLM is achieved by providing it functions and the freedom to call them. So, now the LLM is in total control, it can ask for functions to be run, get results, ask for new functions to be run and so on. This is the second aspect of the schema that makes this LLM system like an OS. Below we have an example of MemGPT storing and recalling important information from the external context that stores chat history.

Image source: ([Packer et al., 2024](https://arxiv.org/abs/2310.08560))

### System Prompt to Generate a MemGPT Type Chatbot

The MemGPT schema shown above can be represented by a system prompt. The system prompt is presented sequentially in the tabs below with a short commentary on each section describing their main features.

*   [General context](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-1)
*   [Conversation Style](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-2)
*   [Setting a chatbot clock](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-3)
*   [Internal and external responses](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-1903177ca82)
*   [Memory management and role definitions](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-1903177cf3f)
*   [Long-term memory access function definition](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-1903177d51f)
*   [Core memory editing functions defined](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-1903177d877)
*   [Long-term memory editing functions defined](https://learning.elucidat.com/go/RGVIL3ZUdVVhZUpxRHJrdHNMa1B5NzVZTzRNNC9HcVhzVVJCYWlIVTk1RkVBRFVWME9XeFBuWlBXSnVkRU9lUzIyM1VvUE5FeXRNMTJHUmJmS29lY3ZFbkpXcTdGTExKaE9QNU9hakJPcWxremFVc1V4VzVUZXplZTQzTkduOSs3MDhRVHoyZitWRVNXS0tIQ0xSTlZhOUVKRHNIaS9MN3kvcDNwZm9wY2hRPQ%3D%3D?i=M0phMnJxR0E0MEpReDZXazl5MnVVTjNjcE5vQXFoTEVJTnRVakxuOHYzajZ0REZQRS9SWE02UXpMRU5Dc05law==&p=UVZ2MlUrK2NlWFVVNEgvTzVZVXRBUT09#pa_6672f21594a29_p1903158424c-tab__pane-1903177dbb0)

*You are MemGPT.*

*Your task is to converse with a user from the perspective of your persona.*

*You are a special memory-based AI that has access to a small core memory, an infinite archival memory, as well as your entire previous conversation history with the user inside of recall memory.*

*Remember that unlike a human, you have to explicitly call functions to view your archival or recall memory.*

*Sometimes, there will be information inside archival or recall memory that is not immediately viewable in the conversation window or in core memory.*

*You are proactive and eagerly search your past conversations to create engaging conversation with the user.*

  

In this section of the system prompt the LLM chatbot is being directed to adopt a persona for conversing with the user.

It outlines the general memory capabilities; it will have *small core memory* & *infinite archival memory* as well as *recall memory* function.

It also instructs the LLM chatbot to search beyond the core memory when carrying out tasks.

Source: ([Hugging Face, n.d.](https://huggingface.co/datasets/MemGPT/function-call-traces))

### Did You Know

Prefix prompting is now being used to control what prompts generate. These prefixes can be random words which have a certain effect on the LLM such that more accurate results are produced.
