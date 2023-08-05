// Copyright (c) 2014, German Neuroinformatics Node (G-Node)
//
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted under the terms of the BSD License. See
// LICENSE file in the root of the Project.

#ifndef NIXPY_ACCESSOR_H
#define NIXPY_ACCESSOR_H


#define GETTER(type, class, name) static_cast<type(class::*)()const>(&class::name)

#define SETTER(type, class, name) static_cast<void(class::*)(const type)>(&class::name)

#define REMOVER(type, class, name) static_cast<bool(class::*)(const type&)>(&class::name)

#define CHECKER(type, class, name) static_cast<bool(class::*)(const type&)const>(&class::name)

#define REF_SETTER(type, class, name) static_cast<void(class::*)(const type&)>(&class::name)

#define OPT_GETTER(type, class, name) static_cast<boost::optional<type>(class::*)()const>(&class::name)

#define DEF_ENT_GETTER(type, class, name, getter_name) \
    static boost::optional<type> getter_name(const class& obj) { \
         type val = obj.name(); \
         if (val) \
             return boost::optional<type>(val); \
         else \
             return boost::none; \
    }

#define DEF_ENT_GETTER_BY(type, class, name, ident_type, getter_name) \
    static boost::optional<type> getter_name(const class& obj, const ident_type& ident) { \
        type val = obj.name(ident); \
        if (val) \
            return boost::optional<type>(val); \
        else \
            return boost::none; \
    }

#define DEF_OPT_SETTER(type, class, name, setter_name) \
    static void setter_name(class& obj, const boost::optional<type>& val) { \
        if (val == boost::none) \
            obj.name(boost::none); \
        else \
            obj.name(*val); \
    }


#endif // NIXPY_ACCESSOR_H
