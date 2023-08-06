#ifndef FIX64VECTOR3_H
#define FIX64VECTOR3_H

#include "Fix64Scalar.h"


struct Fix64Vector3
{
	union
	{

		Fix64Scalar m_vec[3];
		struct {
			Fix64Scalar m_x;
			Fix64Scalar m_y;
			Fix64Scalar m_z;
		};
	};

	Fix64Scalar getX() const
	{
		return m_x;
	}
	
	void setX(Fix64Scalar x)
	{
		m_x=x;
	}

	Fix64Scalar getY() const
	{
		return m_y;
	}
	void setY(Fix64Scalar y)
	{
		m_y=y;
	}

	Fix64Scalar getZ() const
	{
		return m_z;
	}
	void setZ(Fix64Scalar z)
	{
		m_z=z;
	}
	void setValue(const Fix64Scalar&x, const Fix64Scalar&y, const Fix64Scalar&z)
	{
		m_x=x;
		m_y=y;
		m_z=z;
	}

	static Fix64Vector3 makeIdentity()
	{
		Fix64Vector3 res;
		res.setValue(Fix64Scalar::zero(),Fix64Scalar::zero(),Fix64Scalar::zero());
		return res;
	}

	static Fix64Vector3 makeUnitZ()
	{
		Fix64Vector3 res;
		res.setValue(Fix64Scalar::zero(),Fix64Scalar::zero(),Fix64Scalar::one());
		return res;
	}
	static Fix64Vector3 create(const Fix64Scalar&x, const Fix64Scalar&y, const Fix64Scalar&z)
	{
		Fix64Vector3 res;
		res.setValue(x,y,z);
		return res;
	}

	B3_FORCE_INLINE Fix64Scalar dot(const Fix64Vector3& other) const
	{
		Fix64Scalar res = getX()*other.getX()+getY()*other.getY()+getZ()*other.getZ();
		return res;
	}

	static Fix64Scalar dot2(const Fix64Vector3& a, const Fix64Vector3& other)
	{
		Fix64Scalar res = a.getX()*other.getX() + a.getY()*other.getY() + a.getZ()*other.getZ();
		return res;
	}


	B3_FORCE_INLINE Fix64Vector3 cross(const Fix64Vector3& v) const
	{
		return Fix64Vector3::create(
			m_y * v.m_z - m_z * v.m_y,
			m_z * v.m_x - m_x * v.m_z,
			m_x * v.m_y - m_y * v.m_x);
	}

	static Fix64Vector3 cross2(const Fix64Vector3& a, const Fix64Vector3& v)
	{
		return Fix64Vector3::create(
			a.m_y * v.m_z - a.m_z * v.m_y,
			a.m_z * v.m_x - a.m_x * v.m_z,
			a.m_x * v.m_y - a.m_y * v.m_x);
	}

	B3_FORCE_INLINE Fix64Scalar length() const
	{
		Fix64Scalar res = (*this).dot(*this);
		res = Fix64Scalar::sqrt(res);
		return res;
	}
	
	

	B3_FORCE_INLINE Fix64Vector3& operator+=(const Fix64Vector3& v)
	{
		m_x += v.m_x;
		m_y += v.m_y;
		m_z += v.m_z;
		return *this;
	}

	B3_FORCE_INLINE Fix64Vector3 operator-() const
	{
		Fix64Vector3 v = Fix64Vector3::create(-getX(),-getY(),-getZ());
		return v;
	}

	SIMD_FORCE_INLINE Fix64Scalar&       operator[](int i)       
	{
		switch (i)
		{
		case 0:
			{
				return m_x;
			}
		case 1:
			{
				return m_y;
			}
		case 2:
			{
				return m_z;
			}
		default:
			{
			}
		}
		btAssert(0)
		return m_x;
	}
	
	SIMD_FORCE_INLINE const Fix64Scalar operator[](int i) const 
	{ 
		switch (i)
		{
		case 0:
			{
				return m_x;
			}
		case 1:
			{
				return m_y;
			}
		case 2:
			{
				return m_z;
			}
		default:
			{
			}
		}
		btAssert(0)
		return Fix64Scalar::maxValue();
	}

	
};

Fix64Vector3 Fix64MakeVector3(btScalar x,btScalar y,btScalar z)
{
	Fix64Vector3 res = Fix64Vector3::create(Fix64Scalar::fromScalar(x),
		Fix64Scalar::fromScalar(y),
		Fix64Scalar::fromScalar(z));
	return res;
	
}

B3_FORCE_INLINE Fix64Vector3 operator*(const Fix64Scalar& a,const Fix64Vector3& b)
{
	Fix64Vector3 res =Fix64Vector3::create(a*b.getX(),
		a*b.getY(),
		a*b.getZ());
	return res;
}

B3_FORCE_INLINE Fix64Vector3 operator*(const Fix64Vector3& b, const Fix64Scalar& a)
{
	Fix64Vector3 res =Fix64Vector3::create(a*b.getX(),
		a*b.getY(),
		a*b.getZ());
	return res;
}

B3_FORCE_INLINE Fix64Vector3 operator-(const Fix64Vector3& a,const Fix64Vector3& b)
{
	Fix64Vector3 res =Fix64Vector3::create(a.getX()-b.getX(),
		a.getY()-b.getY(),
		a.getZ()-b.getZ());
	return res;
}

B3_FORCE_INLINE Fix64Vector3 operator+(const Fix64Vector3& a,const Fix64Vector3& b)
{
	Fix64Vector3 res =Fix64Vector3::create(a.getX()+b.getX(),
		a.getY()+b.getY(),
		a.getZ()+b.getZ());
	return res;
}




inline const Fix64Vector3 copySignPerElem( const Fix64Vector3 & vec0, const Fix64Vector3 & vec1 )
{
    return Fix64Vector3::create(
		( vec1.getX() < Fix64Scalar::zero() )? -Fix64Abs( vec0.getX() ) : Fix64Abs( vec0.getX() ),
        ( vec1.getY() < Fix64Scalar::zero() )? -Fix64Abs( vec0.getY() ) : Fix64Abs( vec0.getY() ),
        ( vec1.getZ() < Fix64Scalar::zero() )? -Fix64Abs( vec0.getZ() ) : Fix64Abs( vec0.getZ() )
    );
}

inline const Fix64Vector3 mulPerElem( const Fix64Vector3 & vec0, const Fix64Vector3 & vec1 )
{
    return Fix64Vector3::create(
        ( vec0.getX() * vec1.getX() ),
        ( vec0.getY() * vec1.getY() ),
        ( vec0.getZ() * vec1.getZ() )
    );
}




inline const Fix64Vector3 absPerElem( const Fix64Vector3& vec )
{
	return Fix64Vector3::create(Fix64Abs(vec.getX()),Fix64Abs(vec.getY()),Fix64Abs(vec.getZ()));
}


#endif
